"""Utils methods for miners"""


def format_commit_id_date(project_id, start_date, end_date, commit_hash=None):
    """Formats commit query with id and dates
    :param project_id: the project unique identifier
    :param start_date: timestamp, commit start_date
    :param end_date: timestamp, commit end_date
    :param ccommit_hash: optional, if given the query
      filters by commit hash
    :returns: query filter string and where clause
    """
    com_filter, where = "", ""
    if project_id and not commit_hash:
        com_filter += """{{project_id: "{0}"}}""".format(project_id)
    if project_id and commit_hash:
        com_filter += """{{project_id: "{0}", hash: {1}}}""".format(
            project_id, commit_hash)
    if start_date:
        where += "c.timestamp >= {0}".format(start_date)
    if end_date:
        where += " AND " if where else ""
        where += "c.timestamp <= {0}".format(end_date)
    where = "WHERE " + where if where else where

    return com_filter, where
