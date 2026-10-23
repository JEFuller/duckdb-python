import subprocess
import sys
import textwrap


def test_timestamps_work_without_pytz(tmp_path):
    script = """
        import sys
        from importlib.abc import MetaPathFinder

        class BlockPytz(MetaPathFinder):
            def find_spec(self, fullname, path=None, target=None):
                if fullname.partition(".")[0] == "pytz":
                    raise ModuleNotFoundError(fullname, name=fullname)
                return None

        sys.meta_path.insert(0, BlockPytz())
        import site
        site.main()

        import datetime
        from zoneinfo import ZoneInfo
        import duckdb

        with duckdb.connect() as con:
            con.execute("SET TimeZone = 'America/New_York'")
            values = con.execute(
                "SELECT t FROM (VALUES "
                "(TIMESTAMPTZ '2024-11-03 05:30:00+00'), "
                "(TIMESTAMPTZ '2024-11-03 06:30:00+00')) AS times(t) ORDER BY t"
            ).fetchall()
            for (value,), fold, offset in zip(values, (0, 1), (-4, -5)):
                assert isinstance(value.tzinfo, ZoneInfo)
                assert value.tzinfo.key == "America/New_York"
                assert (value.hour, value.minute, value.fold) == (1, 30, fold)
                assert value.utcoffset() == datetime.timedelta(hours=offset)
                assert con.execute("SELECT $1::TIMESTAMPTZ = $2::TIMESTAMPTZ",
                                   [value, value.astimezone(datetime.timezone.utc)]).fetchone() == (True,)

            con.create_function("year_of", lambda value: value.year, ["TIMESTAMPTZ"], "INTEGER")
            assert con.execute("SELECT year_of(TIMESTAMPTZ '2024-01-02 00:00:00+00')").fetchone() == (2024,)
            con.execute("SET TimeZone = 'UTC'")
            value = con.execute("SELECT TIMESTAMPTZ '2024-01-02 03:04:05+00'").fetchone()[0]
            assert value == datetime.datetime(2024, 1, 2, 3, 4, 5, tzinfo=ZoneInfo("UTC"))
            assert isinstance(value.tzinfo, ZoneInfo)
        assert "pytz" not in sys.modules
    """
    proc = subprocess.run(
        [sys.executable, "-S", "-c", textwrap.dedent(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
