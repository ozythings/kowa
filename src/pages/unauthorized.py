from dash import html

def unauthorized_layout():
    return html.Div(className="flex flex-col items-center justify-center h-screen bg-gray-100", children=[
        html.H1(className="text-4xl font-extrabold text-red-600 mb-6", children="Unauthorized"),
        html.P(className="text-xl text-gray-700", children="Please log in to view the dashboard."),
        html.P(className="text-sm text-gray-500 mt-2", children="If you believe this is an error, please contact support."),
    ])
