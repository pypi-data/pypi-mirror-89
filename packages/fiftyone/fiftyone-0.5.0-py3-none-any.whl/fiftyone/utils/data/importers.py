"""
Dataset importers.

| Copyright 2017-2020, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import os

import eta.core.datasets as etads
import eta.core.image as etai
import eta.core.serial as etas
import eta.core.utils as etau

import fiftyone.core.labels as fol
import fiftyone.core.sample as fos
import fiftyone.core.metadata as fom

from .parsers import (
    FiftyOneImageClassificationSampleParser,
    FiftyOneImageDetectionSampleParser,
    FiftyOneImageLabelsSampleParser,
    ImageClassificationSampleParser,
)


class DatasetImporter(object):
    """Base interface for importing datasets stored on disk into FiftyOne.

    .. automethod:: __len__
    .. automethod:: __next__

    Args:
        dataset_dir: the dataset directory
    """

    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, *args):
        self.close(*args)

    def __iter__(self):
        return self

    def __len__(self):
        """The total number of samples that will be imported.

        Raises:
            TypeError: if the total number is not known
        """
        raise TypeError(
            "The number of samples in a '%s' is not known a priori"
            % etau.get_class_name(self)
        )

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            subclass-specific information for the sample

        Raises:
            StopIteration: if there are no more samples to import
        """
        raise NotImplementedError("subclass must implement __next__()")

    def setup(self):
        """Performs any necessary setup before importing the first sample in
        the dataset.

        This method is called when the importer's context manager interface is
        entered, :func:`DatasetImporter.__enter__`.
        """
        pass

    def close(self, *args):
        """Performs any necessary actions after the last sample has been
        imported.

        This method is called when the importer's context manager interface is
        exited, :func:`DatasetImporter.__exit__`.

        Args:
            *args: the arguments to :func:`DatasetImporter.__exit__`
        """
        pass


class GenericSampleDatasetImporter(DatasetImporter):
    """Interface for importing datasets that contain arbitrary
    :class:`fiftyone.core.sample.Sample` instances.

    .. automethod:: __len__
    .. automethod:: __next__

    Example Usage::

        import fiftyone as fo

        dataset = fo.Dataset(...)

        importer = GenericSampleDatasetImporter(dataset_dir, ...)
        with importer:
            for sample in importer:
                dataset.add_sample(sample)

    Args:
        dataset_dir: the dataset directory
    """

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            a :class:`fiftyone.core.sample.Sample` instance

        Raises:
            StopIteration: if there are no more samples to import
        """
        raise NotImplementedError("subclass must implement __next__()")


class UnlabeledImageDatasetImporter(DatasetImporter):
    """Interface for importing datasets of unlabeled image samples.

    .. automethod:: __len__
    .. automethod:: __next__

    Example Usage::

        import fiftyone as fo

        dataset = fo.Dataset(...)

        importer = UnlabeledImageDatasetImporter(dataset_dir, ...)
        with importer:
            for image_path, image_metadata in importer:
                dataset.add_sample(
                    fo.Sample(filepath=image_path, metadata=image_metadata)
                )

    Args:
        dataset_dir: the dataset directory
    """

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            an ``(image_path, image_metadata)`` tuple, where

            -   ``image_path``: the path to the image on disk
            -   ``image_metadata``: an
                :class:`fiftyone.core.metadata.ImageMetadata` instances for the
                image, or ``None`` if :meth:`has_image_metadata` is ``False``

        Raises:
            StopIteration: if there are no more samples to import
        """
        raise NotImplementedError("subclass must implement __next__()")

    @property
    def has_image_metadata(self):
        """Whether this importer produces
        :class:`fiftyone.core.metadata.ImageMetadata` instances for each image.
        """
        raise NotImplementedError("subclass must implement has_image_metadata")


class LabeledImageDatasetImporter(DatasetImporter):
    """Interface for importing datasets of labeled image samples.

    .. automethod:: __len__
    .. automethod:: __next__

    Example Usage::

        import fiftyone as fo

        dataset = fo.Dataset(...)
        label_field = ...

        importer = LabeledImageDatasetImporter(dataset_dir, ...)
        with importer:
            for image_path, image_metadata, label in importer:
                sample = fo.Sample(
                    filepath=image_path, metadata=image_metadata,
                }

                if label is not None:
                    sample[label_field] = label

                dataset.add_sample(sample)

    Args:
        dataset_dir: the dataset directory
    """

    def __next__(self):
        """Returns information about the next sample in the dataset.

        Returns:
            an  ``(image_path, image_metadata, label)`` tuple, where

            -   ``image_path``: the path to the image on disk
            -   ``image_metadata``: an
                :class:`fiftyone.core.metadata.ImageMetadata` instances for the
                image, or ``None`` if :meth:`has_image_metadata` is ``False``
            -   ``label``: an instance of :meth:`label_cls`, or ``None`` if no
                label is available for the sample

        Raises:
            StopIteration: if there are no more samples to import
        """
        raise NotImplementedError("subclass must implement __next__()")

    @property
    def has_image_metadata(self):
        """Whether this importer produces
        :class:`fiftyone.core.metadata.ImageMetadata` instances for each image.
        """
        raise NotImplementedError("subclass must implement has_image_metadata")

    @property
    def label_cls(self):
        """The :class:`fiftyone.core.labels.Label` class returned by this
        importer.
        """
        raise NotImplementedError("subclass must implement label_cls")


class FiftyOneDatasetImporter(GenericSampleDatasetImporter):
    """Importer for FiftyOne datasets stored on disk in serialized format.

    See :class:`fiftyone.types.dataset_types.FiftyOneDataset` for format
    details.

    Args:
        dataset_dir: the dataset directory
    """

    def __init__(self, dataset_dir):
        dataset_dir = os.path.abspath(os.path.expanduser(dataset_dir))
        super().__init__(dataset_dir)
        self._samples = None
        self._iter_samples = None

    def __iter__(self):
        self._iter_samples = iter(self._samples)
        return self

    def __len__(self):
        return len(self._samples)

    def __next__(self):
        """Returns the next sample in the dataset.

        Returns:
            a :class:`fiftyone.core.sample.Sample`

        Raises:
            StopIteration: if there are no more samples to import
        """
        d = next(self._iter_samples)

        # Convert filepath to absolute path
        d["filepath"] = os.path.join(self.dataset_dir, d["filepath"])

        return fos.Sample.from_dict(d)

    def setup(self):
        samples_path = os.path.join(self.dataset_dir, "samples.json")
        self._samples = etas.load_json(samples_path).get("samples", [])


class ImageDirectoryImporter(UnlabeledImageDatasetImporter):
    """Importer for a directory of images stored on disk.

    See :class:`fiftyone.types.dataset_types.ImageDirectory` for format
    details.

    Args:
        dataset_dir: the dataset directory
        recursive (True): whether to recursively traverse subdirectories
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, recursive=True, compute_metadata=False):
        super().__init__(dataset_dir)
        self.recursive = recursive
        self.compute_metadata = compute_metadata
        self._filepaths = None
        self._iter_filepaths = None

    def __iter__(self):
        self._iter_filepaths = iter(self._filepaths)
        return self

    def __len__(self):
        return len(self._filepaths)

    def __next__(self):
        image_path = next(self._iter_filepaths)

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    def setup(self):
        filepaths = etau.list_files(
            self.dataset_dir, abs_paths=True, recursive=self.recursive
        )
        self._filepaths = [p for p in filepaths if etai.is_image_mime_type(p)]


class FiftyOneImageClassificationDatasetImporter(LabeledImageDatasetImporter):
    """Importer for image classification datasets stored on disk in FiftyOne's
    default format.

    See :class:`fiftyone.types.dataset_types.FiftyOneImageClassificationDataset`
    for format details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._image_paths_map = None
        self._labels = None
        self._iter_labels = None
        self._num_samples = None

    def __iter__(self):
        self._iter_labels = iter(self._labels.items())
        return self

    def __len__(self):
        return self._num_samples

    def __next__(self):
        uuid, target = next(self._iter_labels)
        image_path = self._image_paths_map[uuid]

        self._sample_parser.with_sample((image_path, target))
        label = self._sample_parser.get_label()

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.Classification

    def setup(self):
        self._sample_parser = FiftyOneImageClassificationSampleParser()

        data_dir = os.path.join(self.dataset_dir, "data")
        self._image_paths_map = {
            os.path.splitext(os.path.basename(p))[0]: p
            for p in etau.list_files(data_dir, abs_paths=True)
        }

        labels_path = os.path.join(self.dataset_dir, "labels.json")
        labels = etas.load_json(labels_path)
        self._sample_parser.classes = labels.get("classes", None)
        self._labels = labels.get("labels", {})
        self._num_samples = len(self._labels)


class ImageClassificationDirectoryTreeImporter(LabeledImageDatasetImporter):
    """Importer for an image classification directory tree stored on disk.

    See :class:`fiftyone.types.dataset_types.ImageClassificationDirectoryTree`
    for format details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._samples = None
        self._iter_samples = None

    def __iter__(self):
        self._iter_samples = iter(self._samples)
        return self

    def __len__(self):
        return len(self._samples)

    def __next__(self):
        sample = next(self._iter_samples)

        self._sample_parser.with_sample(sample)
        image_path = self._sample_parser.get_image_path()
        label = self._sample_parser.get_label()

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.Classification

    def setup(self):
        self._sample_parser = ImageClassificationSampleParser()

        self._samples = []
        glob_patt = os.path.join(self.dataset_dir, "*", "*")
        for path in etau.get_glob_matches(glob_patt):
            chunks = path.split(os.path.sep)
            if any(s.startswith(".") for s in chunks[-2:]):
                continue

            label = chunks[-2]
            self._samples.append((path, label))


class FiftyOneImageDetectionDatasetImporter(LabeledImageDatasetImporter):
    """Importer for image detection datasets stored on disk in FiftyOne's
    default format.

    See :class:`fiftyone.types.dataset_types.FiftyOneImageDetectionDataset` for
    format details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._image_paths_map = None
        self._labels = None
        self._iter_labels = None
        self._num_samples = None
        self._has_labels = False

    def __iter__(self):
        self._iter_labels = iter(self._labels.items())
        return self

    def __len__(self):
        return self._num_samples

    def __next__(self):
        uuid, target = next(self._iter_labels)
        image_path = self._image_paths_map[uuid]

        if self._has_labels:
            self._sample_parser.with_sample((image_path, target))
            label = self._sample_parser.get_label()
        else:
            label = None

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.Detections

    def setup(self):
        self._sample_parser = FiftyOneImageDetectionSampleParser()

        data_dir = os.path.join(self.dataset_dir, "data")
        self._image_paths_map = {
            os.path.splitext(os.path.basename(p))[0]: p
            for p in etau.list_files(data_dir, abs_paths=True)
        }

        labels_path = os.path.join(self.dataset_dir, "labels.json")
        labels = etas.load_json(labels_path)
        self._sample_parser.classes = labels.get("classes", None)
        self._labels = labels.get("labels", {})
        self._has_labels = any(self._labels.values())
        self._num_samples = len(self._labels)


class FiftyOneImageLabelsDatasetImporter(LabeledImageDatasetImporter):
    """Importer for image labels datasets stored on disk in FiftyOne's default
    format.

    See :class:`fiftyone.types.dataset_types.FiftyOneImageLabelsDataset` for
    format details.

    Args:
        dataset_dir: the dataset directory
        compute_metadata (False): whether to produce
            :class:`fiftyone.core.metadata.ImageMetadata` instances for each
            image when importing
    """

    def __init__(self, dataset_dir, compute_metadata=False):
        super().__init__(dataset_dir)
        self.compute_metadata = compute_metadata
        self._sample_parser = None
        self._labeled_dataset = None
        self._iter_labeled_dataset = None

    def __iter__(self):
        self._iter_labeled_dataset = zip(
            self._labeled_dataset.iter_data_paths(),
            self._labeled_dataset.iter_labels(),
        )
        return self

    def __len__(self):
        return len(self._labeled_dataset)

    def __next__(self):
        sample = next(self._iter_labeled_dataset)

        self._sample_parser.with_sample(sample)
        image_path = self._sample_parser.get_image_path()
        label = self._sample_parser.get_label()

        if self.compute_metadata:
            image_metadata = fom.ImageMetadata.build_for(image_path)
        else:
            image_metadata = None

        return image_path, image_metadata, label

    @property
    def has_image_metadata(self):
        return self.compute_metadata

    @property
    def label_cls(self):
        return fol.ImageLabels

    def setup(self):
        self._sample_parser = FiftyOneImageLabelsSampleParser()
        self._labeled_dataset = etads.load_dataset(self.dataset_dir)
