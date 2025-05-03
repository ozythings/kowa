from dash import html

from i18n.unauthorized_labels import get_unauthorized_labels

def unauthorized_layout(lang="en"):
    labels = get_unauthorized_labels(lang)

    return html.Div(className="flex flex-col items-center justify-center h-screen bg-gray-100", children=[
        html.H1(className="text-4xl font-extrabold text-red-600 mb-6", children=labels["title"]),
        html.P(className="text-xl text-gray-700", children=labels["message"]),
        html.P(className="text-sm text-gray-500 mt-2", children=labels["note"]),
    ])
