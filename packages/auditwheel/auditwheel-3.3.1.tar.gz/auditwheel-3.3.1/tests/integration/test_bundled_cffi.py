import platform
import pytest
from auditwheel.wheel_abi import analyze_wheel_abi


@pytest.mark.skipif(platform.machine() != 'x86_64', reason='only supported on x86_64')
def test_analyze_wheel_abi():
    winfo = analyze_wheel_abi('tests/integration/cffi-1.5.0-cp27-none-linux_x86_64.whl')
    external_libs = winfo.external_refs['manylinux1_x86_64']['libs']
    assert len(external_libs) > 0
    assert set(external_libs) == {'libffi.so.5'}
