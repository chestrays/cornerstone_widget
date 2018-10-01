import json

from cornerstone_widget import get_bbox_handles
from cornerstone_widget.utils import inject_dict

_test_bbox_json = """
{"imageIdToolState": {"": {"rectangleRoi": {"data": [{"visible": true, "active": false, "invalidated": false, "handles": {"start": {"x": 553.3138489596392, "y": 449.722433543228, "highlight": true, "active": false}, "end": {"x": 835.5569648554714, "y": 705.8887398182495, "highlight": true, "active": false}, "textBox": {"active": false, "hasMoved": false, "movesIndependently": false, "drawnIndependently": true, "allowedOutsideImage": true, "hasBoundingBox": true, "x": 835.5569648554714, "y": 577.8055866807388, "boundingBox": {"width": 150.8333282470703, "height": 65, "left": 312.93333435058605, "top": 195.39999389648438}}}, "meanStdDev": {"count": 72731, "mean": 137.81189589033562, "variance": 484.0080783665253, "stdDev": 22.00018359847311}, "area": 72301.17647058812}]}}}, "elementToolState": {}, "elementViewport": {}, "viewing_time": 77.17544794082642}
"""

_test_bbox_json_2 = """
{"imageIdToolState": {"": {"rectangleRoi": {"data": [{"visible": true, "active": false, "invalidated": false, "handles": {"start": {"x": 196.03125, "y": 417.8125, "highlight": true, "active": false}, "end": {"x": 478.03125, "y": 625.8125, "highlight": true, "active": false}, "textBox": {"active": false, "hasMoved": false, "movesIndependently": false, "drawnIndependently": true, "allowedOutsideImage": true, "hasBoundingBox": true, "x": 478.03125, "y": 521.8125, "boundingBox": {"width": 150.9033203125, "height": 65, "left": 239.015625, "top": 228.40625}}}, "meanStdDev": {"count": 58656, "mean": 145.6067352181388, "variance": 1398.8774714024185, "stdDev": 37.40157044032267}, "area": 58656}, {"visible": true, "active": true, "invalidated": false, "handles": {"start": {"x": 658.03125, "y": 497.8125, "highlight": true, "active": false}, "end": {"x": 912.03125, "y": 577.8125, "highlight": true, "active": false}, "textBox": {"active": false, "hasMoved": false, "movesIndependently": false, "drawnIndependently": true, "allowedOutsideImage": true, "hasBoundingBox": true, "x": 912.03125, "y": 537.8125, "boundingBox": {"width": 150.9033203125, "height": 65, "left": 456.015625, "top": 236.40625}}}, "meanStdDev": {"count": 20320, "mean": 136.35415690597338, "variance": 813.4574721617173, "stdDev": 28.521175855173244}, "area": 20320}]}}}, "elementToolState": {}, "elementViewport": {}, "viewing_time": 63.09548878669739}"""


def test_bbox_parser():
    a_bbox = get_bbox_handles(json.loads(_test_bbox_json))
    assert len(a_bbox) == 1
    assert len(a_bbox[0]['x']) == 2
    assert a_bbox[0]['x'][0] > 500
    assert a_bbox[0]['x'][1] < 900
    b_bbox = get_bbox_handles(json.loads(_test_bbox_json_2))
    assert len(b_bbox) == 2
    assert b_bbox[0]['x'][0] < 200
    assert b_bbox[0]['x'][1] > 450


def test_inject():
    n_dict = json.loads(_test_bbox_json)
    n_bbox = [{'handles': {'start': {'x': 0, 'y': 5},
                           'end': {'x': 0, 'y': 5}}}]
    m_dict = inject_dict(n_dict, ['imageIdToolState',
                                  '',
                                  'rectangleRoi',
                                  'data'],
                         n_bbox)
    m_bbox = get_bbox_handles(m_dict)
    print(m_bbox)

    assert len(m_bbox) == 2
    assert m_bbox[1]['x'][0] == 0
