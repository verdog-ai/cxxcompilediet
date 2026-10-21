from verdog_ai.cxxcompilediet import diet, measure


def rec(start: float, end: float, rss: float) -> measure.Record:
    return measure.Record(out="x.o", start=start, end=end, rss_mb=rss)


def test_peak_sums_overlapping_commands_only():
    records = [rec(0, 10, 100), rec(5, 15, 200), rec(10, 20, 50)]
    # 0-5: 100, 5-10: 300, 10-15: 250 (first ended before third started)
    assert measure.peak(records) == 300


def test_summary():
    s = measure.summarize([rec(0, 2, 100), rec(1, 4, 300)], 7.0)
    assert s == measure.Summary(
        peak_rss_mb=400, max_tu_rss_mb=300, sum_tu_seconds=5, build_seconds=7
    )


def test_gain():
    assert diet.gain(200, 150) == 0.25
    assert diet.gain(200, 220) < 0
    assert diet.gain(0, 10) == 0
