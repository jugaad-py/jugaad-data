import os
import pickle
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from jugaad_data.util import cached


def test_atomic_write_no_corruption(monkeypatch):
    """Verify that concurrent cache writes produce valid, readable files."""
    app_name = "test-atomic-write"

    @cached(app_name)
    def fetch_data(key):
        return {"key": key, "value": "data"}

    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setenv("J_CACHE_DIR", tmpdir)

        results = []
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [ex.submit(fetch_data, key=i) for i in range(50)]
            for f in as_completed(futures):
                results.append(f.result())

    assert len(results) == 50
    for r in results:
        assert "key" in r
        assert r["value"] == "data"

    # Verify no stale .tmp files left behind
    cache_dir = os.path.join(tmpdir, app_name)
    if os.path.isdir(cache_dir):
        tmp_files = [f for f in os.listdir(cache_dir) if f.endswith(".tmp")]
        assert len(tmp_files) == 0, f"Stale .tmp files found: {tmp_files}"


def test_concurrent_same_key_does_not_corrupt(monkeypatch):
    """Multiple threads writing the same cache key must produce a valid file."""
    app_name = "test-same-key"

    @cached(app_name)
    def same_key(value):
        return [1, 2, 3, 4, 5]

    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setenv("J_CACHE_DIR", tmpdir)

        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = [ex.submit(same_key, value="static") for _ in range(100)]
            for f in as_completed(futures):
                assert f.result() == [1, 2, 3, 4, 5]

        # Verify persisted file is valid
        cache_dir = os.path.join(tmpdir, app_name)
        for fname in os.listdir(cache_dir):
            fpath = os.path.join(cache_dir, fname)
            with open(fpath, "rb") as fp:
                data = pickle.load(fp)
            assert data == [1, 2, 3, 4, 5]
