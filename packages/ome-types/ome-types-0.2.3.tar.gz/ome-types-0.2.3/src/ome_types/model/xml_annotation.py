from dataclasses import field
from typing import Any, List, Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .annotation_ref import AnnotationRef
from .text_annotation import TextAnnotation


@ome_dataclass
class XMLAnnotation(TextAnnotation):
    """An general xml annotation.

    The contents of this is not processed as OME XML but should still be well-
    formed XML.

    Parameters
    ----------
    value : Any
    annotation_ref : AnnotationRef, optional
    annotator : ExperimenterID, optional
        The Annotator is the person who attached this annotation. e.g. If
        UserA annotates something with TagB, owned by UserB, UserA is still
        the Annotator.
    description : str, optional
        A description for the annotation.
    id : AnnotationID
    namespace : str, optional
        We recommend the inclusion of a namespace for annotations you define.
        If it is absent then we assume the annotation is to use our (OME's)
        default interpretation for this type.
    """

    value: Any = EMPTY  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None

    def __getstate__(self: Any):
        """Support pickle of our weakref references."""
        from ome_types.schema import ElementTree

        d = self.__dict__.copy()
        d["value"] = ElementTree.tostring(d.pop("value")).strip()
        return d

    def __setstate__(self: Any, state) -> None:
        """Support unpickle of our weakref references."""
        from ome_types.schema import ElementTree

        self.__dict__.update(state)
        self.value = ElementTree.fromstring(self.value)

    def __eq__(self, o: "XMLAnnotation") -> bool:
        return self.__getstate__() == o.__getstate__()
