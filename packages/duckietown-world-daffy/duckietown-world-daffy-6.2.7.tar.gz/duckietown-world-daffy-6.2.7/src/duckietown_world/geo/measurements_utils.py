# coding=utf-8
import networkx as nx
import numpy as np
from dataclasses import dataclass
from duckietown_world.seqs import GenericSequence
from networkx import MultiDiGraph
from typing import Callable, Generic, Iterator, List, Tuple, Type, TypeVar

from .placed_object import FQN, PlacedObject, SpatialRelation
from .rectangular_area import RectangularArea
from .transforms import TransformSequence, VariableTransformSequence

__all__ = [
    "iterate_measurements_relations",
    "get_meausurements_graph",
    "get_extent_points",
    "get_static_and_dynamic",
    "iterate_by_class",
    "IterateByTestResult",
]


def iterate_measurements_relations(po_name: FQN, po: PlacedObject) -> Iterator[Tuple[FQN, SpatialRelation]]:
    assert isinstance(po_name, tuple)
    for sr_name, sr in po.spatial_relations.items():
        a = po_name + sr.a
        b = po_name + sr.b
        klass = type(sr)
        # noinspection PyArgumentList
        s = klass(a=a, b=b, transform=sr.transform)
        yield po_name + (sr_name,), s

    for child_name, child in po.children.items():
        cname = po_name + (child_name,)
        yield from iterate_measurements_relations(cname, child)


def get_meausurements_graph(po: PlacedObject) -> MultiDiGraph:
    G = MultiDiGraph()
    for name, sr in iterate_measurements_relations((), po):
        a = sr.a
        b = sr.b
        attr_dict = dict(sr=sr)
        G.add_edge(a, b, attr_dict=attr_dict)
    return G


def get_static_and_dynamic(po: PlacedObject) -> Tuple[List, List]:
    assert isinstance(po, PlacedObject)

    G = get_flattened_measurement_graph(po)

    static = [()]

    dynamic = []
    root_name = ()
    for name in G.nodes():
        if name == root_name:
            continue
        edge_data = G.get_edge_data(root_name, name)

        transform = edge_data["transform_sequence"]
        from duckietown_world.world_duckietown.transformations import is_static

        it_is = is_static(transform)

        if it_is:
            static.append(name)
        else:
            dynamic.append(name)

    return static, dynamic


def get_flattened_measurement_graph(po: PlacedObject, include_root_to_self: bool = False) -> nx.DiGraph:
    from duckietown_world import TransformSequence
    from duckietown_world import SE2Transform

    G = get_meausurements_graph(po)
    G2 = nx.DiGraph()
    root_name = ()
    for name in G.nodes():
        if name == root_name:
            continue
        path = nx.shortest_path(G, (), name)
        transforms = []
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            edges = G.get_edge_data(a, b)

            k = list(edges)[0]
            v = edges[k]
            sr = v["attr_dict"]["sr"].transform

            transforms.append(sr)

        if any(isinstance(_, GenericSequence) for _ in transforms):
            res = VariableTransformSequence(transforms)
        else:
            res = TransformSequence(transforms)
        G2.add_edge(root_name, name, transform_sequence=res)

    if include_root_to_self:
        transform_sequence = SE2Transform.identity()
        G2.add_edge(root_name, root_name, transform_sequence=transform_sequence)

    return G2


X = TypeVar("X")


@dataclass
class IterateByTestResult(Generic[X]):
    fqn: Tuple[str, ...]
    transform_sequence: TransformSequence
    object: X
    parents: Tuple[PlacedObject, ...]


def iterate_by_class(po: PlacedObject, klass: Type[X]) -> Iterator[IterateByTestResult]:
    t = lambda _: isinstance(_, klass)
    yield from iterate_by_test(po, t)


def iterate_by_test(po: PlacedObject, testf: Callable[[PlacedObject], bool]) -> Iterator[IterateByTestResult]:
    G = get_flattened_measurement_graph(po, include_root_to_self=True)
    root_name = ()

    for name in G:
        ob = po.get_object_from_fqn(name)

        if testf(ob):
            transform_sequence = G.get_edge_data(root_name, name)["transform_sequence"]

            parents = get_parents(po, name)

            yield IterateByTestResult(
                fqn=name, transform_sequence=transform_sequence, object=ob, parents=parents,
            )


def get_parents(root: PlacedObject, child_fqn: FQN) -> Tuple[PlacedObject]:
    parents = []
    n = len(child_fqn)
    for i in range(0, n - 1):
        name_parent: FQN = child_fqn[:i]
        parent = root.get_object_from_fqn(name_parent)
        parents.append(parent)
    return tuple(parents)


def get_extent_points(root: PlacedObject) -> RectangularArea:
    G = get_flattened_measurement_graph(root, include_root_to_self=True)
    points = []

    root_name = ()
    for name in G.nodes():

        transform_sequence = G.get_edge_data(root_name, name)["transform_sequence"]
        extent_points = root.get_object_from_fqn(name).extent_points()
        m2d = transform_sequence.asmatrix2d()
        for _ in extent_points:
            p = np.dot(m2d.m, [_[0], _[1], 1])[:2]
            points.append(p)

    if not points:
        msg = "No points"
        raise ValueError(msg)

    pmin = points[0]
    pmax = points[0]

    for p in points:
        pmin = np.minimum(pmin, p)
        pmax = np.maximum(pmax, p)

    return RectangularArea(pmin, pmax)
