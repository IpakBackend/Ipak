from typing import Any

import yaml
from django.core.management.base import BaseCommand

from ...models import Color


class Command(BaseCommand):
    help: str = "Create initial colors"

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.create_default_colors()

    def create_default_colors(self) -> None:
        with open("apps/shops/fixtures/colors.yaml", 'r', encoding="utf-8") as file:
            colors_data: dict[str, list[dict[str, str]]] | None =\
                yaml.safe_load(stream=file)
            if colors_data is not None:
                for color in colors_data.get("colors", []):
                    color_name: str = color["name"].lower()
                    color_hex: str = color["hex"].capitalize()

                    _, created = Color.objects.get_or_create(
                        name=color_name, hex_value=color_hex
                    )

                    if created:
                        self.stdout.write(msg=self.style.SUCCESS(
                            text=f"Color {color_name.capitalize()} created successfully with hexadecimal value {color_hex}"
                        ))
