import pytest
import os


def test_definition_syntax_error(cli, data_dir):
    ee_def = os.path.join(data_dir, 'definition_files', 'invalid.yml')
    r = cli(
        f'ansible-builder build -f {ee_def} --container-runtime podman',
        allow_error=True
    )
    assert r.rc != 0
    assert 'An error occured while parsing the definition file' in (r.stdout + r.stderr), (r.stdout + r.stderr)


def test_build_fail_exitcode(cli, container_runtime, ee_tag, tmpdir, data_dir):
    """Test that when a build fails, the ansible-builder exits with non-zero exit code.

    Example: https://github.com/ansible/ansible-builder/issues/51
    """
    bc = str(tmpdir)
    ee_def = os.path.join(data_dir, 'build_fail', 'execution-environment.yml')
    r = cli(
        f"ansible-builder build -c {bc} -f {ee_def} -t {ee_tag} --container-runtime {container_runtime} -v3",
        allow_error=True
    )
    assert r.rc != 0
    assert 'RUN thisisnotacommand' in (r.stdout + r.stderr), (r.stdout + r.stderr)
    assert 'thisisnotacommand: command not found' in (r.stdout + r.stderr), (r.stdout + r.stderr)


def test_missing_python_requirements_file():
    """If a user specifies a python requirements file, but we can't find it, fail sanely."""
    pytest.skip("Not implemented")


def test_missing_galaxy_requirements_file():
    """If a user specifies a galaxy requirements file, but we can't find it, fail sanely."""
    pytest.skip("Not implemented")


def test_build_streams_output_with_verbosity_on(cli, container_runtime, build_dir_and_ee_yml, ee_tag):
    """Test that 'ansible-builder build' streams build output."""
    tmpdir, eeyml = build_dir_and_ee_yml("")
    result = cli(f"ansible-builder build -c {tmpdir} -f {eeyml} -t {ee_tag} --container-runtime {container_runtime} -v 3")
    assert f'{container_runtime} build -f {tmpdir}' in result.stdout
    assert f'Ansible Builder is building your execution environment image, "{ee_tag}".' in result.stdout
    assert f'The build context can be found at: {tmpdir}' in result.stdout


def test_build_streams_output_with_verbosity_off(cli, container_runtime, build_dir_and_ee_yml, ee_tag):
    """
    Like the test_build_streams_output_with_verbosity_on test but making sure less output is shown with default verbosity level of 2.
    """
    tmpdir, eeyml = build_dir_and_ee_yml("")
    result = cli(f"ansible-builder build -c {tmpdir} -f {eeyml} -t {ee_tag} --container-runtime {container_runtime}")
    assert f'Ansible Builder is building your execution environment image, "{ee_tag}".' not in result.stdout
    assert f'The build context can be found at: {tmpdir}' in result.stdout


def test_build_streams_output_with_invalid_verbosity(cli, container_runtime, build_dir_and_ee_yml, ee_tag):
    """
    Like the test_build_streams_output_with_verbosity_off test but making sure it errors out correctly with invalid verbosity level.
    """
    tmpdir, eeyml = build_dir_and_ee_yml("")
    result = cli(f"ansible-builder build -c {tmpdir} -f {eeyml} -t {ee_tag} --container-runtime {container_runtime} -v 6", allow_error=True)
    assert result.rc != 0
    assert 'invalid choice: 6 (choose from 0, 1, 2, 3)' in (result.stdout + result.stderr)


def test_blank_execution_environment(cli, container_runtime, ee_tag, tmpdir, data_dir):
    """Just makes sure that the buld process does not require any particular input"""
    bc = str(tmpdir)
    ee_def = os.path.join(data_dir, 'blank', 'execution-environment.yml')
    cli(
        f'ansible-builder build -c {bc} -f {ee_def} -t {ee_tag} --container-runtime {container_runtime}'
    )
    result = cli(f'{container_runtime} run --rm {ee_tag} echo "This is a simple test"')
    assert 'This is a simple test' in result.stdout, result.stdout


def test_user_system_requirement(cli, container_runtime, ee_tag, tmpdir, data_dir):
    bc = str(tmpdir)
    ee_def = os.path.join(data_dir, 'subversion', 'execution-environment.yml')
    command = f'ansible-builder build -c {bc} -f {ee_def} -t {ee_tag} --container-runtime {container_runtime}'
    cli(command)
    result = cli(
        f'{container_runtime} run --rm {ee_tag} svn --help'
    )
    assert 'Subversion is a tool for version control' in result.stdout, result.stdout


def test_collection_system_requirement(cli, container_runtime, ee_tag, tmpdir, data_dir):
    bc = str(tmpdir)
    ee_def = os.path.join(data_dir, 'ansible.posix.at', 'execution-environment.yml')
    cli(
        f'ansible-builder build -c {bc} -f {ee_def} -t {ee_tag} --container-runtime {container_runtime} -v3'
    )
    result = cli(
        f'{container_runtime} run --rm {ee_tag} at -V'
    )
    assert 'at version' in result.stderr, result.stderr


def test_user_python_requirement(cli, container_runtime, ee_tag, tmpdir, data_dir):
    bc = str(tmpdir)
    ee_def = os.path.join(data_dir, 'pip', 'execution-environment.yml')
    command = f'ansible-builder build -c {bc} -f {ee_def} -t {ee_tag} --container-runtime {container_runtime}'
    cli(command)
    result = cli(
        f'{container_runtime} run --rm {ee_tag} pip3 show awxkit'
    )
    assert 'The official command line interface for Ansible AWX' in result.stdout, result.stdout


def test_prepended_steps(cli, container_runtime, ee_tag, tmpdir, data_dir):
    """
    Tests that prepended steps are in final stage
    """
    bc = str(tmpdir)
    ee_def = os.path.join(data_dir, 'prepend_steps', 'execution-environment.yml')
    cli(
        f'ansible-builder build -c {bc} -f {ee_def} -t {ee_tag} --container-runtime {container_runtime}'
    )

    _file = 'Dockerfile' if container_runtime == 'docker' else 'Containerfile'
    content = open(os.path.join(bc, _file), 'r').read()

    stages_content = content.split('FROM')

    assert 'RUN whoami' in stages_content[-1]


class TestPytz:

    @pytest.fixture(scope='class')
    def pytz(self, cli_class, container_runtime, ee_tag_class, data_dir, tmpdir_factory):
        bc_folder = str(tmpdir_factory.mktemp('bc'))
        ee_def = os.path.join(data_dir, 'pytz', 'execution-environment.yml')
        r = cli_class(
            f'ansible-builder build -c {bc_folder} -f {ee_def} -t {ee_tag_class} --container-runtime {container_runtime} -v 3'
        )
        assert 'Collecting pytz' in r.stdout, r.stdout
        return (ee_tag_class, bc_folder)

    def test_has_pytz(self, cli, container_runtime, pytz):
        ee_tag, bc_folder = pytz
        r = cli(f'{container_runtime} run --rm {ee_tag} pip3 show pytz')
        assert 'World timezone definitions, modern and historical' in r.stdout, r.stdout

    def test_build_layer_reuse(self, cli, container_runtime, data_dir, pytz):
        ee_tag, bc_folder = pytz
        ee_def = os.path.join(data_dir, 'pytz', 'execution-environment.yml')
        r = cli(
            f'ansible-builder build -c {bc_folder} -f {ee_def} -t {ee_tag} --container-runtime {container_runtime} -v 3'
        )
        assert 'Collecting pytz (from -r /build/' not in r.stdout, r.stdout
        assert 'requirements_combined.txt is already up-to-date' in r.stdout, r.stdout
        stdout_no_whitespace = r.stdout.replace('--->', '-->').replace('\n', ' ').replace('   ', ' ').replace('  ', ' ')
        assert 'RUN /output/install-from-bindep --> Using cache' in stdout_no_whitespace, r.stdout
