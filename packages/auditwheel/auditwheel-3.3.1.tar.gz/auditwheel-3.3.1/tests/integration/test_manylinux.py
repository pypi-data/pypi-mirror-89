import glob
from contextlib import contextmanager
import docker
from subprocess import CalledProcessError
import pytest
import io
import os
import os.path as op
import re
import shutil
import sys
import logging
import zipfile
from auditwheel.policy import get_priority_by_name, get_arch_name
from elftools.elf.elffile import ELFFile


logger = logging.getLogger(__name__)


ENCODING = 'utf-8'
PLATFORM = get_arch_name()
MANYLINUX1_IMAGE_ID = f'quay.io/pypa/manylinux1_{PLATFORM}'
MANYLINUX2010_IMAGE_ID = f'quay.io/pypa/manylinux2010_{PLATFORM}'
MANYLINUX2014_IMAGE_ID = f'quay.io/pypa/manylinux2014_{PLATFORM}:latest'
if PLATFORM in {'i686', 'x86_64'}:
    MANYLINUX_IMAGES = {
        'manylinux1': MANYLINUX1_IMAGE_ID,
        'manylinux2010': MANYLINUX2010_IMAGE_ID,
        'manylinux2014': MANYLINUX2014_IMAGE_ID,
    }
else:
    MANYLINUX_IMAGES = {
        'manylinux2014': MANYLINUX2014_IMAGE_ID,
    }
DOCKER_CONTAINER_NAME = 'auditwheel-test-manylinux'
PYTHON_MAJ_MIN = [str(i) for i in sys.version_info[:2]]
PYTHON_ABI_MAJ_MIN = ''.join(PYTHON_MAJ_MIN)
PYTHON_ABI_FLAGS = 'm' if sys.version_info.minor < 8 else ''
PYTHON_ABI = f'cp{PYTHON_ABI_MAJ_MIN}-cp{PYTHON_ABI_MAJ_MIN}{PYTHON_ABI_FLAGS}'
PYTHON_IMAGE_ID = 'python:' + '.'.join(PYTHON_MAJ_MIN)
DEVTOOLSET = {
    'manylinux1': 'devtoolset-2',
    'manylinux2010': 'devtoolset-8',
    'manylinux2014': 'devtoolset-9',
}
PATH_DIRS = [
    f'/opt/python/{PYTHON_ABI}/bin',
    '/opt/rh/{devtoolset}/root/usr/bin',
    '/usr/local/sbin',
    '/usr/local/bin',
    '/usr/sbin',
    '/usr/bin',
    '/sbin',
    '/bin',
]
PATH = {k: ':'.join(PATH_DIRS).format(devtoolset=v)
        for k, v in DEVTOOLSET.items()}
WHEEL_CACHE_FOLDER = op.expanduser('~/.cache/auditwheel_tests')
NUMPY_VERSION = '1.19.2'
ORIGINAL_NUMPY_WHEEL = f'numpy-{NUMPY_VERSION}-{PYTHON_ABI}-linux_{PLATFORM}.whl'
ORIGINAL_SIX_WHEEL = 'six-1.11.0-py2.py3-none-any.whl'


def find_src_folder():
    candidate = op.abspath(op.join(op.dirname(__file__), '../..'))
    contents = os.listdir(candidate)
    if 'setup.py' in contents and 'auditwheel' in contents:
        return candidate


def docker_start(image, volumes={}, env_variables={}):
    """Start a long waiting idle program in container

    Return the container object to be used for 'docker exec' commands.
    """
    # Make sure to use the latest public version of the docker image
    client = docker.from_env()

    dvolumes = {host: {'bind': ctr, 'mode': 'rw'}
                for (ctr, host) in volumes.items()}

    logger.info("Starting container with image %r", image)
    con = client.containers.run(image, ['sleep', '10000'], detach=True,
                                volumes=dvolumes, environment=env_variables)
    logger.info("Started container %s", con.id[:12])
    return con


@contextmanager
def docker_container_ctx(image, io_dir=None, env_variables={}):
    src_folder = find_src_folder()
    if src_folder is None:
        pytest.skip('Can only be run from the source folder')
    vols = {'/auditwheel_src': src_folder}
    if io_dir is not None:
        vols['/io'] = io_dir

    for key in env_variables:
        if key.startswith('COV_CORE_'):
            env_variables[key] = env_variables[key].replace(src_folder,
                                                            '/auditwheel_src')

    container = docker_start(image, vols, env_variables)
    try:
        yield container
    finally:
        container.remove(force=True)


def docker_exec(container, cmd, expected_retcode=0):
    logger.info("docker exec %s: %r", container.id[:12], cmd)
    ec, output = container.exec_run(cmd)
    output = output.decode(ENCODING)
    if ec != expected_retcode:
        print(output)
        raise CalledProcessError(ec, cmd, output=output)
    return output


@pytest.fixture()
def io_folder(tmp_path):
    d = tmp_path / 'io'
    d.mkdir(exist_ok=True)
    return str(d)

@contextmanager
def tmp_docker_image(base, commands, setup_env={}):
    """Make a temporary docker image for tests

    Pulls the *base* image, runs *commands* inside it with *setup_env*, and
    commits the result as a new image. The image is removed on exiting the
    context.

    Making temporary images like this avoids each test having to re-run the
    same container setup steps.
    """
    with docker_container_ctx(base, env_variables=setup_env) as con:
        for cmd in commands:
            docker_exec(con, cmd)
        image = con.commit()

    logger.info("Made image %s based on %s", image.short_id, base)
    try:
        yield image.short_id
    finally:
        client = image.client
        client.images.remove(image.id)

@pytest.fixture(scope='session')
def docker_python_img():
    """The Python base image with up-to-date pip"""
    with tmp_docker_image(PYTHON_IMAGE_ID, ['pip install pip']) as img_id:
        yield img_id

@pytest.fixture(scope='session', params=MANYLINUX_IMAGES.keys())
def any_manylinux_img(request):
    """Each manylinux image, with auditwheel installed.

    Plus up-to-date pip, setuptools and pytest-cov
    """
    policy = request.param
    base = MANYLINUX_IMAGES[policy]
    env = {'PATH': PATH[policy]}
    with tmp_docker_image(base, [
        'pip install -U pip setuptools pytest-cov',
        'pip install -U -e /auditwheel_src',
    ], env) as img_id:
        yield policy, img_id

@pytest.fixture()
def docker_python(docker_python_img, io_folder):
    with docker_container_ctx(docker_python_img, io_folder) as container:
        yield container


@pytest.fixture()
def any_manylinux_container(any_manylinux_img, io_folder):
    policy, manylinux_img = any_manylinux_img
    env = {'PATH': PATH[policy]}
    for key in os.environ:
        if key.startswith('COV_CORE_'):
            env[key] = os.environ[key]

    with docker_container_ctx(manylinux_img, io_folder, env) as container:
        yield f'{policy}_{PLATFORM}', container


def test_build_repair_numpy(any_manylinux_container, docker_python, io_folder):
    # Integration test: repair numpy built from scratch

    # First build numpy from source as a naive linux wheel that is tied
    # to system libraries (atlas, libgfortran...)
    policy, manylinux_ctr = any_manylinux_container
    docker_exec(manylinux_ctr, 'yum install -y atlas atlas-devel')

    if op.exists(op.join(WHEEL_CACHE_FOLDER, policy, ORIGINAL_NUMPY_WHEEL)):
        # If numpy has already been built and put in cache, let's reuse this.
        shutil.copy2(op.join(WHEEL_CACHE_FOLDER, policy, ORIGINAL_NUMPY_WHEEL),
                     op.join(io_folder, ORIGINAL_NUMPY_WHEEL))
    else:
        # otherwise build the original linux_x86_64 numpy wheel from source
        # and put the result in the cache folder to speed-up future build.
        # This part of the build is independent of the auditwheel code-base
        # so it's safe to put it in cache.
        docker_exec(
            manylinux_ctr,
            f'pip wheel -w /io --no-binary=:all: numpy=={NUMPY_VERSION}'
        )
        os.makedirs(op.join(WHEEL_CACHE_FOLDER, policy), exist_ok=True)
        shutil.copy2(op.join(io_folder, ORIGINAL_NUMPY_WHEEL),
                     op.join(WHEEL_CACHE_FOLDER, policy, ORIGINAL_NUMPY_WHEEL))
    filenames = os.listdir(io_folder)
    assert filenames == [ORIGINAL_NUMPY_WHEEL]
    orig_wheel = filenames[0]
    assert 'manylinux' not in orig_wheel

    # Repair the wheel using the manylinux container
    repair_command = f'auditwheel repair --plat {policy} -w /io /io/{orig_wheel}'
    docker_exec(manylinux_ctr, repair_command)
    filenames = os.listdir(io_folder)

    assert len(filenames) == 2
    repaired_wheels = [fn for fn in filenames if 'manylinux' in fn]
    assert repaired_wheels == [
        f'numpy-{NUMPY_VERSION}-{PYTHON_ABI}-{policy}.whl'
    ]
    repaired_wheel = repaired_wheels[0]
    output = docker_exec(manylinux_ctr, 'auditwheel show /io/' + repaired_wheel)
    assert (
        f'numpy-{NUMPY_VERSION}-{PYTHON_ABI}-{policy}.whl is consistent'
        f' with the following platform tag: "{policy}"'
    ) in output.replace('\n', ' ')

    # Check that the repaired numpy wheel can be installed and executed
    # on a modern linux image.
    docker_exec(docker_python, 'pip install /io/' + repaired_wheel)
    output = docker_exec(docker_python,
        'python /auditwheel_src/tests/integration/quick_check_numpy.py')
    assert output.strip() == 'ok'

    # Check that numpy f2py works with a more recent version of gfortran
    docker_exec(docker_python, 'apt-get update -yqq')
    docker_exec(docker_python, 'apt-get install -y gfortran')
    docker_exec(docker_python, 'python -m numpy.f2py'
                           ' -c /auditwheel_src/tests/integration/foo.f90 -m foo')

    # Check that the 2 fortran runtimes are well isolated and can be loaded
    # at once in the same Python program:
    docker_exec(docker_python, ["python", "-c", "'import numpy; import foo'"])


def test_build_wheel_with_binary_executable(any_manylinux_container, docker_python,
                                            io_folder):
    # Test building a wheel that contains a binary executable (e.g., a program)

    policy, manylinux_ctr = any_manylinux_container
    docker_exec(manylinux_ctr, 'yum install -y gsl-devel')

    docker_exec(
        manylinux_ctr,
        ['bash', '-c', 'cd /auditwheel_src/tests/integration/testpackage && python -m pip wheel --no-deps -w /io .']
    )

    filenames = os.listdir(io_folder)
    assert filenames == ['testpackage-0.0.1-py3-none-any.whl']
    orig_wheel = filenames[0]
    assert 'manylinux' not in orig_wheel

    # Repair the wheel using the appropriate manylinux container
    repair_command = f'auditwheel repair --plat {policy} -w /io /io/{orig_wheel}'
    docker_exec(manylinux_ctr, repair_command)
    filenames = os.listdir(io_folder)
    assert len(filenames) == 2
    repaired_wheels = [fn for fn in filenames if policy in fn]
    # Wheel picks up newer symbols when built in manylinux2010
    expected_wheel_name = f'testpackage-0.0.1-py3-none-{policy}.whl'
    assert repaired_wheels == [expected_wheel_name]
    repaired_wheel = repaired_wheels[0]
    output = docker_exec(manylinux_ctr, 'auditwheel show /io/' + repaired_wheel)
    assert (
        f'testpackage-0.0.1-py3-none-{policy}.whl is consistent'
        f' with the following platform tag: "{policy}"'
    ) in output.replace('\n', ' ')

    docker_exec(docker_python, 'pip install /io/' + repaired_wheel)
    output = docker_exec(
        docker_python,
        ['python', '-c', 'from testpackage import runit; print(runit(1.5))']
    )
    assert output.strip() == '2.25'


@pytest.mark.parametrize('with_dependency', ['0', '1'])
def test_build_wheel_with_image_dependencies(with_dependency, any_manylinux_container, docker_python,
                                             io_folder):
    # try to repair the wheel targeting different policies
    #
    # with_dependency == 0
    #   The python module has no dependencies that should be grafted-in and
    #   uses versioned symbols not available on policies pre-dating the policy
    #   matching the image being tested.
    # with_dependency == 1
    #   The python module itself does not use versioned symbols but has a
    #   dependency that should be grafted-in that uses versioned symbols not
    #   available on policies pre-dating the policy matching the image being
    #   tested.

    policy, manylinux_ctr = any_manylinux_container

    docker_exec(manylinux_ctr, [
        'bash', '-c',
        'cd /auditwheel_src/tests/integration/testdependencies && '
        f'WITH_DEPENDENCY={with_dependency} python setup.py -v build_ext -f '
        'bdist_wheel -d /io'])

    filenames = os.listdir(io_folder)
    orig_wheel = filenames[0]
    assert 'manylinux' not in orig_wheel

    repair_command = \
        'LD_LIBRARY_PATH=/auditwheel_src/tests/integration/testdependencies:$LD_LIBRARY_PATH '\
        'auditwheel -v repair --plat {policy} -w /io /io/{orig_wheel}'

    policy_priority = get_priority_by_name(policy)
    older_policies = \
        [p for p in MANYLINUX_IMAGES.keys()
         if policy_priority < get_priority_by_name(f'{p}_{PLATFORM}')]
    for target_policy in older_policies:
        # we shall fail to repair the wheel when targeting an older policy than
        # the one matching the image
        with pytest.raises(CalledProcessError):
            docker_exec(manylinux_ctr, [
                'bash',
                '-c',
                repair_command.format(policy=target_policy,
                                      orig_wheel=orig_wheel)])

    # check all works properly when targeting the policy matching the image
    docker_exec(manylinux_ctr, [
        'bash', '-c',
        repair_command.format(policy=policy, orig_wheel=orig_wheel)])
    filenames = os.listdir(io_folder)
    assert len(filenames) == 2
    repaired_wheels = [fn for fn in filenames if policy in fn]
    expected_wheel_name = f'testdependencies-0.0.1-{PYTHON_ABI}-{policy}.whl'
    assert repaired_wheels == [expected_wheel_name]
    repaired_wheel = repaired_wheels[0]
    output = docker_exec(manylinux_ctr, 'auditwheel show /io/' + repaired_wheel)
    assert (
        f'testdependencies-0.0.1-{PYTHON_ABI}-{policy}.whl is consistent'
        f' with the following platform tag: "{policy}"'
    ) in output.replace('\n', ' ')

    # check the original wheel with a dependency was not compliant
    # and check the one without a dependency was already compliant
    output = docker_exec(manylinux_ctr, 'auditwheel show /io/' + orig_wheel)
    if with_dependency == '1':
        assert (
            f'{orig_wheel} is consistent with the following platform tag: '
            f'"linux_{PLATFORM}"'
        ) in output.replace('\n', ' ')
    else:
        assert (
            f'{orig_wheel} is consistent with the following platform tag: '
            f'"{policy}"'
        ) in output.replace('\n', ' ')

    docker_exec(docker_python, 'pip install /io/' + repaired_wheel)
    docker_exec(
        docker_python,
        ['python', '-c',
         'from sys import exit; from testdependencies import run; exit(run())']
    )


def test_build_repair_pure_wheel(any_manylinux_container, io_folder):
    policy, manylinux_ctr = any_manylinux_container

    if op.exists(op.join(WHEEL_CACHE_FOLDER, policy, ORIGINAL_SIX_WHEEL)):
        # If six has already been built and put in cache, let's reuse this.
        shutil.copy2(op.join(WHEEL_CACHE_FOLDER, policy,  ORIGINAL_SIX_WHEEL),
                     op.join(io_folder, ORIGINAL_SIX_WHEEL))
        logger.info(f"Copied six wheel from {WHEEL_CACHE_FOLDER} to {io_folder}")
    else:
        docker_exec(manylinux_ctr, 'pip wheel -w /io --no-binary=:all: six==1.11.0')
        os.makedirs(op.join(WHEEL_CACHE_FOLDER, policy), exist_ok=True)
        shutil.copy2(op.join(io_folder, ORIGINAL_SIX_WHEEL),
                     op.join(WHEEL_CACHE_FOLDER, policy, ORIGINAL_SIX_WHEEL))

    filenames = os.listdir(io_folder)
    assert filenames == [ORIGINAL_SIX_WHEEL]
    orig_wheel = filenames[0]
    assert 'manylinux' not in orig_wheel

    # Repair the wheel using the manylinux container
    repair_command = f'auditwheel repair --plat {policy} -w /io /io/{orig_wheel}'
    output = docker_exec(manylinux_ctr, repair_command, expected_retcode=1)
    assert "This does not look like a platform wheel" in output

    output = docker_exec(manylinux_ctr, f'auditwheel show /io/{orig_wheel}',
                         expected_retcode=1)
    assert "This does not look like a platform wheel" in output


@pytest.mark.parametrize('dtag', ['rpath', 'runpath'])
def test_build_wheel_depending_on_library_with_rpath(any_manylinux_container, docker_python,
                                                     io_folder, dtag):
    # Test building a wheel that contains an extension depending on a library
    # with RPATH or RUNPATH set.
    # Following checks are performed:
    # - check if RUNPATH is replaced by RPATH
    # - check if RPATH location is correct, i.e. it is inside .libs directory
    #   where all gathered libraries are put

    policy, manylinux_ctr = any_manylinux_container

    docker_exec(
        manylinux_ctr,
        [
            'bash',
            '-c',
            (
                'cd /auditwheel_src/tests/integration/testrpath '
                '&& rm -rf build '
                f'&& DTAG={dtag} python setup.py bdist_wheel -d /io'
            ),
        ]
    )
    with open(op.join(op.dirname(__file__), 'testrpath', 'a', 'liba.so'), 'rb') as f:
        elf = ELFFile(f)
        dynamic = elf.get_section_by_name('.dynamic')
        tags = {t.entry.d_tag for t in dynamic.iter_tags()}
        assert f"DT_{dtag.upper()}" in tags
    filenames = os.listdir(io_folder)
    assert filenames == [f'testrpath-0.0.1-{PYTHON_ABI}-linux_{PLATFORM}.whl']
    orig_wheel = filenames[0]
    assert 'manylinux' not in orig_wheel

    # Repair the wheel using the appropriate manylinux container
    repair_command = f'auditwheel repair --plat {policy} -w /io /io/{orig_wheel}'
    docker_exec(
        manylinux_ctr,
        ['bash', '-c', 'LD_LIBRARY_PATH=/auditwheel_src/tests/integration/testrpath/a:$LD_LIBRARY_PATH ' + repair_command],
    )
    filenames = os.listdir(io_folder)
    repaired_wheels = [fn for fn in filenames if policy in fn]
    # Wheel picks up newer symbols when built in manylinux2010
    expected_wheel_name = f'testrpath-0.0.1-{PYTHON_ABI}-{policy}.whl'
    assert expected_wheel_name in repaired_wheels
    repaired_wheel = expected_wheel_name
    output = docker_exec(manylinux_ctr, 'auditwheel show /io/' + repaired_wheel)
    if PLATFORM in {'x86_64', 'i686'}:
        expect = f'manylinux1_{PLATFORM}'
    else:
        expect = f'manylinux2014_{PLATFORM}'
    assert (
        f'testrpath-0.0.1-{PYTHON_ABI}-{policy}.whl is consistent'
        f' with the following platform tag: "{expect}"'
    ) in output.replace('\n', ' ')

    docker_exec(docker_python, 'pip install /io/' + repaired_wheel)
    output = docker_exec(
        docker_python,
        ['python', '-c', 'from testrpath import testrpath; print(testrpath.func())']
    )
    assert output.strip() == '11'
    with zipfile.ZipFile(os.path.join(io_folder, repaired_wheel)) as w:
        for name in w.namelist():
            if 'testrpath/.libs/lib' in name:
                with w.open(name) as f:
                    elf = ELFFile(io.BytesIO(f.read()))
                    dynamic = elf.get_section_by_name('.dynamic')
                    assert len([t for t in dynamic.iter_tags() if t.entry.d_tag == 'DT_RUNPATH']) == 0
                    if '.libs/liba' in name:
                        rpath_tags = [t for t in dynamic.iter_tags() if t.entry.d_tag == 'DT_RPATH']
                        assert len(rpath_tags) == 1
                        assert rpath_tags[0].rpath == '$ORIGIN/.'


def test_build_repair_multiple_top_level_modules_wheel(any_manylinux_container, docker_python, io_folder):

    policy, manylinux_ctr = any_manylinux_container

    docker_exec(
        manylinux_ctr,
        [
            'bash',
            '-c',
            'cd /auditwheel_src/tests/integration/multiple_top_level '
            '&& make '
            '&& pip wheel . -w /io',
        ]
    )

    filenames = os.listdir(io_folder)
    assert filenames == [
        f'multiple_top_level-1.0-{PYTHON_ABI}-linux_{PLATFORM}.whl']
    orig_wheel = filenames[0]
    assert 'manylinux' not in orig_wheel

    # Repair the wheel using the appropriate manylinux container
    repair_command = f'auditwheel repair --plat {policy} -w /io /io/{orig_wheel}'
    docker_exec(
        manylinux_ctr,
        [
            'bash',
            '-c',
            (
                'LD_LIBRARY_PATH='
                '/auditwheel_src/tests/integration/multiple_top_level/lib-src/a:'
                '/auditwheel_src/tests/integration/multiple_top_level/lib-src/b:'
                '$LD_LIBRARY_PATH '
            )
            + repair_command,
        ],
    )
    filenames = os.listdir(io_folder)
    repaired_wheels = [fn for fn in filenames if policy in fn]
    # Wheel picks up newer symbols when built in manylinux2010
    expected_wheel_name = f'multiple_top_level-1.0-{PYTHON_ABI}-{policy}.whl'
    assert repaired_wheels == [expected_wheel_name]
    repaired_wheel = expected_wheel_name
    output = docker_exec(manylinux_ctr, 'auditwheel show /io/' + repaired_wheel)
    if PLATFORM in {'x86_64', 'i686'}:
        expect = f'manylinux1_{PLATFORM}'
    else:
        expect = f'manylinux2014_{PLATFORM}'
    assert (
        f'{repaired_wheel} is consistent'
        f' with the following platform tag: "{expect}"'
    ) in output.replace('\n', ' ')

    docker_exec(docker_python, 'pip install /io/' + repaired_wheel)
    for mod, func, expected in [
        ('example_a', 'example_a', '11'),
        ('example_b', 'example_b', '110'),
    ]:
        output = docker_exec(
            docker_python,
            [
                'python',
                '-c',
                f'from {mod} import {func}; print({func}())',
            ],
        ).strip()
        assert output.strip() == expected
    with zipfile.ZipFile(os.path.join(io_folder, repaired_wheel)) as w:
        for lib_name in ['liba', 'libb']:
            assert any(
                re.match(
                    rf'multiple_top_level.libs/{lib_name}.*\.so', name
                )
                for name in w.namelist()
            )


def test_build_repair_wheel_with_internal_rpath(any_manylinux_container, docker_python, io_folder):
    

    policy, manylinux_ctr = any_manylinux_container

    docker_exec(
        manylinux_ctr,
        [
            'bash',
            '-c',
            'cd /auditwheel_src/tests/integration/internal_rpath '
            '&& make '
            '&& mv lib-src/a/liba.so internal_rpath'
            '&& pip wheel . -w /io',
        ]
    )

    filenames = os.listdir(io_folder)
    assert filenames == [f'internal_rpath-1.0-{PYTHON_ABI}-linux_{PLATFORM}.whl']
    orig_wheel = filenames[0]
    assert 'manylinux' not in orig_wheel
    
    # Repair the wheel using the appropriate manylinux container
    repair_command = f'auditwheel repair --plat {policy} -w /io /io/{orig_wheel}'
    docker_exec(
        manylinux_ctr,
        [
            'bash',
            '-c',
            (
                'LD_LIBRARY_PATH='
                '/auditwheel_src/tests/integration/internal_rpath/lib-src/b:'
                '$LD_LIBRARY_PATH '
            )
            + repair_command,
        ],
    )
    filenames = os.listdir(io_folder)
    repaired_wheels = [fn for fn in filenames if policy in fn]
    # Wheel picks up newer symbols when built in manylinux2010
    expected_wheel_name = f'internal_rpath-1.0-{PYTHON_ABI}-{policy}.whl'
    assert repaired_wheels == [expected_wheel_name]
    repaired_wheel = expected_wheel_name
    output = docker_exec(manylinux_ctr, 'auditwheel show /io/' + repaired_wheel)
    if PLATFORM in {'x86_64', 'i686'}:
        expect = f'manylinux1_{PLATFORM}'
    else:
        expect = f'manylinux2014_{PLATFORM}'
    assert (
        f'{repaired_wheel} is consistent'
        f' with the following platform tag: "{expect}"'
    ) in output.replace('\n', ' ')

    docker_exec(docker_python, 'pip install /io/' + repaired_wheel)
    for mod, func, expected in [
        ('example_a', 'example_a', '11'),
        ('example_b', 'example_b', '10'),
    ]:
        output = docker_exec(
            docker_python,
            [
                'python',
                '-c',
                f'from internal_rpath.{mod} import {func}; print({func}())',
            ],
        ).strip()
        assert output.strip() == expected
    with zipfile.ZipFile(os.path.join(io_folder, repaired_wheel)) as w:
        for lib_name in ['libb']:
            assert any(
                re.match(
                    rf'internal_rpath.libs/{lib_name}.*\.so', name
                )
                for name in w.namelist()
            )


def test_strip_wheel(any_manylinux_container, docker_python, io_folder):
    policy, manylinux_ctr = any_manylinux_container
    docker_exec(
        manylinux_ctr,
        ['bash', '-c', 'cd /auditwheel_src/tests/integration/sample_extension '
                       '&& python -m pip wheel --no-deps -w /io .']
    )

    orig_wheel, *_ = os.listdir(io_folder)
    assert orig_wheel.startswith("sample_extension-0.1.0")

    # Repair the wheel using the appropriate manylinux container
    repair_command = \
        f'auditwheel repair --plat {policy} --strip -w /io /io/{orig_wheel}'
    docker_exec(manylinux_ctr, repair_command)

    repaired_wheel, *_ = glob.glob(f"{io_folder}/*{policy}*.whl")
    repaired_wheel = os.path.basename(repaired_wheel)

    docker_exec(docker_python, "pip install /io/" + repaired_wheel)
    output = docker_exec(
        docker_python,
        ["python", "-c", "from sample_extension import test_func; print(test_func(1))"]
    )
    assert output.strip() == "2"
