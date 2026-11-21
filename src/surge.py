NO_SURGE_PRODUCTS = {"Shared", "UberPool", "WAV"}
PEAK_HOURS = set(range(7, 10)) | set(range(16, 20))
NIGHT_HOURS = set(range(22, 24)) | set(range(0, 5))
RAIN_ADD = {"none": 0.0, "light": 0.15, "heavy": 0.40}
PEAK_ADD = 0.35
EVENT_ADD = 0.25
NIGHT_WEEKEND_ADD = 0.20
STEP = 0.25
MIN_SURGE = 1.0
MAX_SURGE = 3.0


def compute_surge(product, hour, rain="none", event=False, weekend=False):
    if product in NO_SURGE_PRODUCTS:
        return 1.0
    surge = 1.0
    if hour in PEAK_HOURS:
        surge += PEAK_ADD
    surge += RAIN_ADD[rain]
    if event:
        surge += EVENT_ADD
    if weekend and hour in NIGHT_HOURS:
        surge += NIGHT_WEEKEND_ADD
    surge = round(surge / STEP) * STEP
    return min(max(surge, MIN_SURGE), MAX_SURGE)


if __name__ == "__main__":
    print(compute_surge("UberX", 12))
    print(compute_surge("UberX", 8, rain="heavy"))
    print(compute_surge("UberPool", 8, rain="heavy"))
    print(compute_surge("Lux", 23, rain="light", event=True, weekend=True))
