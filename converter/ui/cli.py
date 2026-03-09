"""
Rich CLI Interface - Terminal UI yang colorful dan interaktif
Menggunakan library Rich untuk display yang menarik
"""

import os
import sys
from pathlib import Path
from typing import Optional, List

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.layout import Layout
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.columns import Columns
except ImportError:
    print("Rich library not found. Please install: pip install rich")
    sys.exit(1)

from converter.config import INPUT_DIR, OUTPUT_DIR
from converter.core.resource_pack_converter import ResourcePackConverter


class ConverterCLI:
    """Command Line Interface untuk Resource Pack Converter"""
    
    # Colors
    COLOR_PRIMARY = "#00D9FF"      # Cyan
    COLOR_SUCCESS = "#00FF00"      # Green
    COLOR_WARNING = "#FFAA00"      # Orange
    COLOR_ERROR = "#FF0000"        # Red
    COLOR_INFO = "#0099FF"         # Blue
    
    def __init__(self):
        """Initialize CLI"""
        self.console = Console()
        self.converter: Optional[ResourcePackConverter] = None
    
    def print_header(self):
        """Print aplikasi header"""
        header = """
 ╔══════════════════════════════════════════════════════════════════════════╗
 ║                  MINECRAFT RESOURCE PACK CONVERTER                       ║
 ║                    Java Edition → Bedrock Edition                        ║
 ║                     Full Support with GeyserMC                           ║
 ╚══════════════════════════════════════════════════════════════════════════╝
        """
        
        self.console.print(header, style="bold cyan")
        self.console.print("\n[bold]Features:[/bold]")
        self.console.print("  ✓ Convert Textures (PNG, JPG → PNG Bedrock)")
        self.console.print("  ✓ Convert Sounds (OGG, WAV, MP3 → OGG Bedrock)")
        self.console.print("  ✓ Convert Models (JSON → Bedrock Format)")
        self.console.print("  ✓ Convert Fonts & Languages")
        self.console.print("  ✓ Create Geyser Mappings (Full Java/Bedrock Support)")
        self.console.print("  ✓ Automatic Manifest Generation")
        self.console.print()
    
    def print_paths_info(self):
        """Print informasi paths"""
        table = Table(title="📁 Project Paths", show_header=True, header_style="bold cyan")
        table.add_column("Type", style="cyan")
        table.add_column("Path", style="green")
        
        table.add_row("Input Directory", str(INPUT_DIR))
        table.add_row("Output Directory", str(OUTPUT_DIR))
        
        self.console.print(table)
        self.console.print()
    
    def list_available_packs(self) -> List[str]:
        """List available resource packs di input directory"""
        packs = []
        
        if not INPUT_DIR.exists():
            INPUT_DIR.mkdir(parents=True, exist_ok=True)
            return packs
        
        for item in INPUT_DIR.iterdir():
            if item.is_dir() and (item / "pack.mcmeta").exists():
                packs.append(item.name)
            elif item.is_file() and item.suffix == ".zip":
                packs.append(item.name)
        
        return sorted(packs)
    
    def show_pack_list(self) -> Optional[str]:
        """Display dan select resource pack"""
        packs = self.list_available_packs()
        
        if not packs:
            self.console.print(
                f"[bold {self.COLOR_ERROR}]No resource packs found in {INPUT_DIR}[/]"
            )
            self.console.print(f"\n[bold yellow]Please place Java resource packs in:[/] {INPUT_DIR}")
            self.console.print("  - Extract your pack folder here, or")
            self.console.print("  - Place pack.zip files here\n")
            return None
        
        # Create table untuk list packs
        table = Table(title="📦 Available Resource Packs", show_header=True, header_style="bold cyan")
        table.add_column("#", style="yellow", width=5)
        table.add_column("Pack Name", style="cyan")
        table.add_column("Status", style="green")
        
        for idx, pack in enumerate(packs, 1):
            pack_path = INPUT_DIR / pack
            if pack_path.is_file():
                status = "[yellow]ZIP File[/]"
            else:
                status = "[green]Folder[/]"
            table.add_row(str(idx), pack, status)
        
        self.console.print(table)
        self.console.print()
        
        # Ask user to select
        while True:
            try:
                choice = Prompt.ask(
                    "[bold cyan]Select pack number (or 'q' to quit)[/]",
                    choices=[str(i) for i in range(1, len(packs) + 1)] + ['q']
                )
                
                if choice == 'q':
                    return None
                
                return packs[int(choice) - 1]
            except (ValueError, IndexError):
                self.console.print("[bold red]Invalid selection[/]\n")
    
    def show_conversion_options(self) -> dict:
        """Show conversion options"""
        options = {
            'compress_textures': False,
            'convert_sounds': True,
            'include_geyser': True,
            'verbose': False,
        }
        
        self.console.print("\n[bold cyan]═════ Conversion Options ═════[/]\n")
        
        # Geyser mapping
        options['include_geyser'] = Confirm.ask(
            "[cyan]Include Geyser mappings for Java/Bedrock compatibility?[/]",
            default=True
        )
        
        # Verbose
        options['verbose'] = Confirm.ask(
            "[cyan]Enable verbose logging?[/]",
            default=False
        )
        
        self.console.print()
        return options
    
    def show_conversion_progress(self, pack_name: str, options: dict) -> bool:
        """Show conversion progress"""
        self.console.print("\n[bold cyan]Starting conversion...[/]\n")
        
        converter = ResourcePackConverter(pack_name, verbose=options['verbose'])
        self.converter = converter
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Converting..."),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console,
                transient=False
            ) as progress:
                task = progress.add_task("conversion", total=100)
                
                # Simulate progress stages
                stages = [
                    (20, "Validating pack..."),
                    (35, "Converting textures..."),
                    (50, "Converting sounds..."),
                    (65, "Converting models..."),
                    (80, "Converting fonts..."),
                    (90, "Creating Geyser mappings..."),
                    (100, "Finalizing..."),
                ]
                
                # Run actual conversion
                success = converter.convert()
                
                # Update progress to 100
                progress.update(task, completed=100)
            
            return success
            
        except Exception as e:
            self.console.print(f"[bold red]Conversion failed: {e}[/]\n")
            return False
    
    def show_results(self, success: bool):
        """Show conversion results"""
        if not self.converter:
            return
        
        stats = self.converter.get_statistics()
        
        if success:
            # Success panel
            success_msg = Panel(
                "[bold green]✓ Conversion Completed Successfully![/]\n"
                f"[yellow]Duration:[/] {stats['duration']:.2f} seconds",
                title="[bold green]SUCCESS[/]",
                border_style="green",
                expand=False
            )
            self.console.print(success_msg)
        else:
            # Error panel
            error_msg = Panel(
                "[bold red]✗ Conversion Failed[/]\n"
                f"[yellow]Status:[/] {stats['status']}",
                title="[bold red]ERROR[/]",
                border_style="red",
                expand=False
            )
            self.console.print(error_msg)
        
        # Statistics table
        self.console.print("\n[bold cyan]═════ Conversion Statistics ═════[/]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Component", style="cyan")
        table.add_column("Count", style="yellow")
        table.add_column("Status", style="green")
        
        table.add_row(
            "Textures",
            str(stats['total_textures']),
            "[green]✓[/]" if stats['total_textures'] > 0 else "[yellow]─[/]"
        )
        table.add_row(
            "Sounds",
            str(stats['total_sounds']),
            "[green]✓[/]" if stats['total_sounds'] > 0 else "[yellow]─[/]"
        )
        table.add_row(
            "Models",
            str(stats['total_models']),
            "[green]✓[/]" if stats['total_models'] > 0 else "[yellow]─[/]"
        )
        table.add_row(
            "Fonts",
            str(stats['total_fonts']),
            "[green]✓[/]" if stats['total_fonts'] > 0 else "[yellow]─[/]"
        )
        
        self.console.print(table)
        
        # Output location
        self.console.print(f"\n[bold cyan]Output Location:[/]")
        self.console.print(f"  [green]{self.converter.bedrock_pack_path}[/]\n")
        
        # Errors/warnings
        if stats['errors']:
            self.console.print(f"[bold yellow]⚠ Errors ({len(stats['errors'])}):[/]")
            for error in stats['errors'][:5]:  # Show first 5
                self.console.print(f"  [red]✗[/] {error}")
            if len(stats['errors']) > 5:
                self.console.print(f"  [dim]... and {len(stats['errors']) - 5} more[/]")
    
    def show_next_steps(self):
        """Show next steps after conversion"""
        self.console.print("\n[bold cyan]═════ Next Steps ═════[/]\n")
        
        steps = [
            "[bold cyan]1. Setup Bedrock Pack:[/]\n   Copy the output folder to your Bedrock resource packs directory",
            
            "[bold cyan]2. Enable in Minecraft:[/]\n   World Settings → Resource Packs → Activate the converted pack",
            
            "[bold cyan]3. For GeyserMC Server:[/]\n   Place pack in GeyserMC/packs/ directory\n   " +
            "Bedrock players will see custom items/blocks automatically",
            
            "[bold cyan]4. Troubleshooting:[/]\n   Check logs in the output folder for any conversion issues",
        ]
        
        for step in steps:
            self.console.print(f"  {step}\n")
    
    def run(self):
        """Main CLI loop"""
        try:
            # Print header
            self.print_header()
            
            # Ensure directories exist
            INPUT_DIR.mkdir(parents=True, exist_ok=True)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            
            # Show paths
            self.print_paths_info()
            
            # Select pack
            pack_name = self.show_pack_list()
            if not pack_name:
                self.console.print("[bold yellow]Conversion cancelled[/]\n")
                return
            
            # Show options
            options = self.show_conversion_options()
            
            # Run conversion
            success = self.show_conversion_progress(pack_name, options)
            
            # Show results
            self.show_results(success)
            
            # Show next steps
            if success:
                self.show_next_steps()
            
            self.console.print("[bold cyan]─" * 36 + "[/]\n")
            
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Conversion cancelled by user[/]\n")
        except Exception as e:
            self.console.print(f"[bold red]Unexpected error: {e}[/]\n")
            if options.get('verbose'):
                import traceback
                traceback.print_exc()


def main():
    """Entry point untuk CLI"""
    cli = ConverterCLI()
    cli.run()


if __name__ == "__main__":
    main()
