import platform
import pytest
from auditwheel.wheel_abi import analyze_wheel_abi


@pytest.mark.skipif(platform.machine() != 'x86_64', reason='only supported on x86_64')
def test_analyze_wheel_abi():
    winfo = analyze_wheel_abi('tests/integration/fpewheel-0.0.0-cp35-cp35m-linux_x86_64.whl')
    assert winfo.sym_tag == 'manylinux1_x86_64'  # for external symbols, it could get manylinux1
    assert winfo.pyfpe_tag == 'linux_x86_64'     # but for having the pyfpe reference, it gets just linux
