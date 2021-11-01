def median_filter_generator(rng):
    def median_filter(data):
        values = []
        for val in data:
            values.append(val)
            if len(values) > rng:
                values = values[1:]
            yield sorted(values)[len(values) // 2]

    return median_filter
