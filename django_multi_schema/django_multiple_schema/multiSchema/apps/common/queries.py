usergoes = ""
fixedPromos = ""


def lanreg():
    query = f"""
    select *
    from language_new as lan
    INNER JOIN regions as reg ON
        lan.region_id = reg.id
    where reg.id in (%s)
    """
    return query


def tenant():
    query = f"""
    select *
    from language_new as lan
    INNER JOIN tenants as ten ON
        lan.tenant_id = ten.id
    where ten.id in (%s)
    """
    return query
