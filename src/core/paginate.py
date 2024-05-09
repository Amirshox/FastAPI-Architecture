def paginate(page: int, page_size: int, total_count: int):
    page_count = total_count // page_size + 1
    return page_count
