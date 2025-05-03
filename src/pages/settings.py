import dash
from dash import html, dcc
from flask import session

from pages.unauthorized import unauthorized_layout

dash.register_page(__name__, path="/settings")

def settings_layout(lang="en"):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                        html.H1(
                            "Settings",
                            className="text-4xl font-bold mb-4"
                        ),
                        html.P(
                            "Adjust your preferences and manage your account settings here. Don't forget to save your changes.",
                            className="text-gray-600 mb-8"
                        ),
                            # profile
                            html.Div(
                                [
                                    html.H2("Profile", className="text-2xl font-semibold mb-4"),
                                    html.H3("Name", className="text-lg font-medium mb-2"),
                                    dcc.Input(
                                        id="profile_name",
                                        type="text",
                                        placeholder="Your name",
                                        required=True,
                                        className="border border-gray-300 rounded p-2 w-full mb-4"
                                    ),
                                    html.H3("Email", className="text-lg font-medium mb-2"),
                                    dcc.Input(
                                        id="profile_email",
                                        type="email",
                                        placeholder="Your email",
                                        required=True,
                                        className="border border-gray-300 rounded p-2 w-full mb-4"
                                    ),
                                    html.Button(
                                        "UPDATE PROFILE",
                                        id="update_profile_button",
                                        className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                                    ),
                                    html.Div(id="update_profile_status", className="mt-4"),
                                ],
                                className="mb-12"
                            ),

                            html.Div(className="border-t border-gray-300 my-8"),

                            # change password
                            html.Div(
                                [
                                    html.H2("Change Password", className="text-2xl font-semibold mb-4"),
                                    html.H3("New Password", className="text-lg font-medium mb-2"),
                                    dcc.Input(
                                        id="new_password",
                                        type="password",
                                        placeholder="Your new password",
                                        required=True,
                                        className="border border-gray-300 rounded p-2 w-full mb-4"
                                    ),
                                    html.H3("Confirm New Password", className="text-lg font-medium mb-2"),
                                    dcc.Input(
                                        id="confirm_new_password",
                                        type="password",
                                        required=True,
                                        className="border border-gray-300 rounded p-2 w-full mb-4"
                                    ),
                                    html.Button(
                                        "UPDATE PASSWORD",
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
                                    html.H2("Delete Account", className="text-2xl font-semibold mb-4 text-red-600"),
                                    html.Button(
                                        "Delete Account",
                                        id="delete_account_button",
                                        className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 mb-4"
                                    ),
                                    html.Div(
                                        [
                                            html.H3("Enter Password to Confirm", className="text-lg font-medium mb-2"),
                                            dcc.Input(
                                                id="confirm_password",
                                                type="password",
                                                required=True,
                                                className="border border-gray-300 rounded p-2 w-full mb-4"
                                            ),
                                            html.Button(
                                                "Confirm Delete",
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
