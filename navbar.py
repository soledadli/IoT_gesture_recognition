import dash_bootstrap_components as dbc
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/index")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Page 2", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Prediction Data",
        color="primary",
        dark=True,
    )
    return navbar
