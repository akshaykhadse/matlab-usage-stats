def pop_ip(path):
    """
    Finds IP for given timestamps from port activity log (tcpdump).

    **Args:**

    *path: String*
        Path for the port activity log (tcpdump) file.

    **Returns:**

    *ip_time_table: Dict*
        Returns a dictionary with time as keys and ip as value.
    """
    ip_time_table = {}
    with open(path) as tcpdump:
        for line in tcpdump:
            if line != '\n':
                data = line.split('   ')
                time_clean = data[0]
                ip_clean = data[1]
                ip_time_table[time_clean] = ip_clean
    return ip_time_table
