"""
Dataset views.

| Copyright 2017-2020, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from copy import copy, deepcopy
import numbers

from bson import ObjectId, json_util

import fiftyone.core.collections as foc
import fiftyone.core.sample as fos
import fiftyone.core.stages as fost


class DatasetView(foc.SampleCollection):
    """A view into a :class:`fiftyone.core.dataset.Dataset`.

    Dataset views represent ordered collections of subsets of samples in a
    dataset.

    Operations on dataset views are designed to be chained together to yield
    the desired subset of the dataset, which is then iterated over to directly
    access the sample views. Each stage in the pipeline defining a dataset view
    is represented by a :class:`fiftyone.core.stages.ViewStage` instance.

    The stages of a dataset view specify:

    -   what subset of samples (and their order) should be included
    -   what "parts" (fields and their elements) of the sample should be
        included

    Samples retrieved from dataset views are returns as
    :class:`fiftyone.core.sample.SampleView` objects, as opposed to
    :class:`fiftyone.core.sample.Sample` objects, since they may contain a
    subset of the sample's content.

    Example use::

        # Print paths for 5 random samples from the test split of a dataset
        view = dataset.match_tag("test").take(5)
        for sample in view:
            print(sample.filepath)

    Args:
        dataset: a :class:`fiftyone.core.dataset.Dataset`
    """

    def __init__(self, dataset):
        self._dataset = dataset
        self._stages = []

    def __len__(self):
        try:
            result = self.aggregate([{"$count": "count"}])
            return next(result)["count"]
        except StopIteration:
            pass

        return 0

    def __getitem__(self, sample_id):
        if isinstance(sample_id, numbers.Integral):
            raise KeyError(
                "Accessing samples by numeric index is not supported. "
                "Use sample IDs or slices"
            )

        if isinstance(sample_id, slice):
            return self._slice(sample_id)

        # Ensure `sample_id` is in the view
        view = self.match({"_id": ObjectId(sample_id)})
        if not view:
            raise KeyError("No sample found with ID '%s'" % sample_id)

        return self._dataset[sample_id]

    def __copy__(self):
        view = self.__class__(self._dataset)
        view._stages = deepcopy(self._stages)
        return view

    @property
    def stages(self):
        """The list of :class:`fiftyone.core.stages.ViewStage` instances in
        this view's pipeline.
        """
        return self._stages

    def summary(self):
        """Returns a string summary of the view.

        Returns:
            a string summary
        """
        fields_str = self._dataset._get_fields_str()

        if self._stages:
            pipeline_str = "    " + "\n    ".join(
                [
                    "%d. %s" % (idx, str(d))
                    for idx, d in enumerate(self._stages, 1)
                ]
            )
        else:
            pipeline_str = "    ---"

        return "\n".join(
            [
                "Dataset:        %s" % self._dataset.name,
                "Num samples:    %d" % len(self),
                "Tags:           %s" % self.get_tags(),
                "Sample fields:",
                fields_str,
                "Pipeline stages:",
                pipeline_str,
            ]
        )

    def iter_samples(self):
        """Returns an iterator over the samples in the view.

        Returns:
            an iterator over :class:`fiftyone.core.sample.SampleView` instances
        """
        selected_fields, excluded_fields = self._get_selected_excluded_fields()
        filtered_fields = self._get_filtered_fields()

        for d in self.aggregate():
            try:
                doc = self._dataset._sample_dict_to_doc(d)
                yield fos.SampleView(
                    doc,
                    selected_fields=selected_fields,
                    excluded_fields=excluded_fields,
                    filtered_fields=filtered_fields,
                )
            except Exception as e:
                raise ValueError(
                    "Failed to load sample from the database. This is likely "
                    "due to an invalid stage in the DatasetView"
                ) from e

    def get_field_schema(self, ftype=None, embedded_doc_type=None):
        """Returns a schema dictionary describing the fields of the samples in
        the view.

        Args:
            ftype (None): an optional field type to which to restrict the
                returned schema. Must be a subclass of
                :class:``fiftyone.core.fields.Field``
            embedded_doc_type (None): an optional embedded document type to
                which to restrict the returned schema. Must be a subclass of
                :class:``fiftyone.core.odm.BaseEmbeddedDocument``

        Returns:
             a dictionary mapping field names to field types
        """
        return self._dataset.get_field_schema(
            ftype=ftype, embedded_doc_type=embedded_doc_type
        )

    def get_tags(self):
        """Returns the list of unique tags of samples in the view.

        Returns:
            a list of tags
        """
        pipeline = [
            {"$project": {"tags": "$tags"}},
            {"$unwind": "$tags"},
            {"$group": {"_id": "None", "all_tags": {"$addToSet": "$tags"}}},
        ]
        try:
            return next(self.aggregate(pipeline))["all_tags"]
        except StopIteration:
            pass

        return []

    def add_stage(self, stage):
        """Adds a :class:`fiftyone.core.stages.ViewStage` to the current view,
        returning a new view.

        Args:
            stage: a :class:`fiftyone.core.stages.ViewStage`
        """
        return self._add_view_stage(stage)

    def aggregate(self, pipeline=None):
        """Calls the view's current MongoDB aggregation pipeline.

        Args:
            pipeline (None): an optional aggregation pipeline (list of dicts)
                to append to the view's pipeline before calling it

        Returns:
            an iterable over the aggregation result
        """
        _pipeline = []
        for s in self._stages:
            _pipeline.extend(s.to_mongo())

        if pipeline is not None:
            _pipeline.extend(pipeline)

        return self._dataset.aggregate(_pipeline)

    def serialize(self):
        """Serializes the view.

        Returns:
            a JSON representation of the view
        """
        return {
            "dataset": self._dataset.serialize(),
            "view": json_util.dumps([s._serialize() for s in self._stages]),
        }

    def to_dict(self):
        """Returns a JSON dictionary representation of the view.

        Returns:
            a JSON dict
        """
        d = {
            "name": self._dataset.name,
            "num_samples": len(self),
            "tags": self.get_tags(),
            "sample_fields": self._dataset._get_fields_dict(),
            "pipeline_stages": [str(d) for d in self._stages],
        }
        d.update(super().to_dict())
        return d

    def _slice(self, s):
        if s.step is not None and s.step != 1:
            raise ValueError(
                "Unsupported slice '%s'; step is not supported" % s
            )

        _len = None

        start = s.start
        if start is not None:
            if start < 0:
                _len = len(self)
                start += _len

            if start <= 0:
                start = None

        stop = s.stop
        if stop is not None and stop < 0:
            if _len is None:
                _len = len(self)

            stop += _len

        if start is None:
            if stop is None:
                return self

            return self.limit(stop)

        if stop is None:
            return self.skip(start)

        return self.skip(start).limit(stop - start)

    def _add_view_stage(self, stage):
        view = copy(self)
        view._stages.append(stage)
        return view

    def _get_selected_excluded_fields(self):
        """Checks all stages to find the selected and excluded fields.

        Returns:
            a tuple of

            -   selected_fields: the set of selected fields
            -   excluded_fields: the set of excluded_fields

            One of these will always be ``None``, meaning nothing is
            selected/excluded
        """
        selected_fields = None
        excluded_fields = set()

        for stage in self._stages:
            if isinstance(stage, fost.SelectFields):
                if selected_fields is None:
                    selected_fields = set(stage.field_names)
                else:
                    selected_fields.intersection_update(stage.field_names)

            if isinstance(stage, fost.ExcludeFields):
                excluded_fields.update(stage.field_names)

        if selected_fields is not None:
            selected_fields.difference_update(excluded_fields)
            excluded_fields = None

        return selected_fields, excluded_fields

    def _get_filtered_fields(self):
        filtered_fields = set()

        for stage in self._stages:
            if isinstance(stage, fost._FilterList):
                filtered_fields.add(stage.list_field)

        return filtered_fields
