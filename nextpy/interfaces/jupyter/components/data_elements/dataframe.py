import pandas as pd
from typing import Optional, List, Dict, Union
import ipyvuetify as v
from IPython.display import display

def dataframe(
    data: Union[pd.DataFrame, List[Dict[str, any]], None] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    use_container_width: bool = False,
    hide_index: Optional[bool] = None,
    column_order: Optional[List[str]] = None,
    column_config: Optional[Dict[str, any]] = None,
    **kwargs,
):
    """
    High-level function to display data as an interactive table using ipyvuetify's DataTable.
    
    :param data: Data to display. Can be a pandas DataFrame or a list of dictionaries.
    :param width: Desired width of the table in pixels.
    :param height: Desired height of the table in pixels.
    :param use_container_width: If True, stretches the table width to match the container's width.
    :param hide_index: If True, hides the DataFrame's index column.
    :param column_order: Specifies the display order of columns.
    :param column_config: Dictionary for additional column configurations.
    :param kwargs: Additional keyword arguments to pass to the DataTable widget.
    """
    
    if isinstance(data, pd.DataFrame):
        if hide_index:
            data.reset_index(drop=True, inplace=True)
        items = data.to_dict('records')
        headers = [{'text': col, 'value': col} for col in (column_order if column_order else data.columns)]
    elif isinstance(data, list):
        items = data
        headers = [{'text': key, 'value': key} for key in data[0].keys()] if data else []
    else:
        raise ValueError("Unsupported data type. Please provide a pandas DataFrame or a list of dictionaries.")
    
   
    if column_config:
        for header in headers:
            col_name = header['value']
            if col_name in column_config:
                header_config = column_config[col_name]
                if isinstance(header_config, str):
                    header['text'] = header_config
                elif isinstance(header_config, dict):
                    header.update(header_config)
    dt = v.DataTable(
        items=items,
        headers=headers,
        dense=True,
        hide_default_footer=hide_index,
        **kwargs
    )
    
    
    style_css = ''
    if width:
        style_css += f'max-width: {width}px; '
    if height:
        style_css += f'max-height: {height}px; '
    if use_container_width:
        style_css += 'width: 100%;'
    
    dt.style_ = style_css

    return dt

