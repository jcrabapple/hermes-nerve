from __future__ import annotations

import importlib.util
from pathlib import Path

from hermes_jev.reflex.laya_service import evaluate

ROOT=Path(__file__).resolve().parents[1]
_spec=importlib.util.spec_from_file_location('dev17_matrix',ROOT/'scripts/run_dev17_model_matrix.py')
_matrix=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_matrix)


def test_completed_is_success_terminal_state():
    assert _matrix.classification('completed','completed',0,0,True,0,0) == 'SUCCESS'
    assert _matrix.classification('done','done',0,0,True,0,0) == 'SUCCESS'


def test_external_and_nerve_kills_have_distinct_taxonomy():
    assert _matrix.classification('blocked','blocked',0,0,True,1,0) == 'HARNESS_KILL'
    assert _matrix.classification('blocked','blocked',0,0,True,0,1,0) == 'NERVE_KILL'
    assert _matrix.classification('review','done',0,0,True,0,0,1) == 'ORCH_REVIEW'
    assert _matrix.classification('done','done',0,0,True,0,0,1) == 'SUCCESS'


def test_verification_and_lifecycle_failures_are_distinct():
    assert _matrix.classification('completed','completed',1,0,True,0,0) == 'VERIFICATION_FAIL'
    assert _matrix.classification('running','running',0,0,True,0,0) == 'LIFECYCLE_FAIL'


def test_laya_service_accepts_predict_only_sdk_shape():
    class Agent:
        def predict(self,state,questions):
            return {'answers':{'q':{'type':'noul','noul':0.8}},'usage':{'input_tokens':3,'output_tokens':0}}
    out=evaluate(Agent(),state='x',questions={'q':{'type':'noul','instructions':'yes?'}},model_name='laya-test')
    assert out['model']=='laya-test'
    assert out['answers']['q']['noul']==0.8
