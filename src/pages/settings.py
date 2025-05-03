import dash
from dash import html, dcc
from flask import session

from i18n.settings_labels import get_settings_labels
from pages.unauthorized import unauthorized_layout

dash.register_page(__name__, path="/settings")

def settings_layout(lang="en"):

    labels = get_settings_labels(lang)

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(
                                labels["title"],
                                className="text-4xl font-bold mb-4"
                            ),
                            html.P(
                                labels["description"],
                                className="text-gray-600 mb-8"
                            ),
                            # profile
                            # html.Div(
                            #     [
                            #         html.H2(labels["profile_section"]["title"], className="text-2xl font-semibold mb-4"),
                            #         html.H3(labels["profile_section"]["name"], className="text-lg font-medium mb-2"),
                            #         dcc.Input(
                            #             id="profile_name",
                            #             type="text",
                            #             placeholder=labels["profile_section"]["name_placeholder"],
                            #             required=True,
                            #             className="border border-gray-300 rounded p-2 w-full mb-4"
                            #         ),
                            #         html.H3(labels["profile_section"]["email"], className="text-lg font-medium mb-2"),
                            #         dcc.Input(
                            #             id="profile_email",
                            #             type="email",
                            #             placeholder=labels["profile_section"]["email_placeholder"],
                            #             required=True,
                            #             className="border border-gray-300 rounded p-2 w-full mb-4"
                            #         ),
                            #         html.Button(
                            #             labels["profile_section"]["update_button"],
                            #             id="update_profile_button",
                            #             className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                            #         ),
                            #         html.Div(id="update_profile_status", className="mt-4"),
                            #     ],
                            #     className="mb-12"
                            # ),

                            html.Div(className="border-t border-gray-300 my-8"),

                            # change password
                            html.Div(
                                [
                                    html.H2(labels["change_password_section"]["title"], className="text-2xl font-semibold mb-4"),
                                    html.H3(labels["change_password_section"]["new_password"], className="text-lg font-medium mb-2"),
                                    dcc.Input(
                                        id="new_password",
                                        type="password",
                                        placeholder=labels["change_password_section"]["new_password_placeholder"],
                                        required=True,
                                        className="border border-gray-300 rounded p-2 w-full mb-4"
                                    ),
                                    html.H3(labels["change_password_section"]["confirm_new_password"], className="text-lg font-medium mb-2"),
                                    dcc.Input(
                                        id="confirm_new_password",
                                        type="password",
                                        required=True,
                                        className="border border-gray-300 rounded p-2 w-full mb-4"
                                    ),
                                    html.Button(
                                        labels["change_password_section"]["update_button"],
                                        id="update_password_button",
                                        className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
                                    ),
                                    html.Div(id="update_password_status", className="mt-4"),
                                ],
                                className="mb-12"
                            ),

                            html.Div(className="border-t border-gray-300 my-8"),

                            # delete account
                            html.Div(
                                [
                                    html.H2(labels["delete_account_section"]["title"], className="text-2xl font-semibold mb-4 text-red-600"),
                                    html.Button(
                                        labels["delete_account_section"]["button"],
                                        id="delete_account_button",
                                        className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 mb-4"
                                    ),
                                    html.Div(
                                        [
                                            html.H3(labels["delete_account_section"]["confirm_label"], className="text-lg font-medium mb-2"),
                                            dcc.Input(
                                                id="confirm_password",
                                                type="password",
                                                required=True,
                                                className="border border-gray-300 rounded p-2 w-full mb-4"
                                            ),
                                            html.Button(
                                                labels["delete_account_section"]["confirm_button"],
                                                id="confirm_delete_button",
                                                className="bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700"
                                            )
                                        ],
                                        id="confirm_delete_section",
                                        className="hidden mt-4"
                                    ),
                                    html.Div(id="delete_status", className="mt-4"),
                                ],
                                className="mb-12"
                            ),
                        ],
                        className="max-w-2xl mx-auto"
                    ),
                ],
                className="p-8"
            ),
        ],
        className="min-h-screen bg-gray-100"
    )

def layout(**page_args):
    if session.get("logged_in"):
        return settings_layout(page_args.get("lang"))
    else:
        return unauthorized_layout(page_args.get("lang"))
