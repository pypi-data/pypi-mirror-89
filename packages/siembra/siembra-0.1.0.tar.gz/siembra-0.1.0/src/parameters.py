

def parse_parameters_dictionary(config):
    # FIXME: Add validation
    return {k: v if v is not None else '' for k, v in config.items()}
