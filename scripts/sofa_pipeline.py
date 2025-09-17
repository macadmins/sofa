#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich>=13.7.0",
#     "typer>=0.9.0",
# ]
# ///
"""
SOFA Pipeline - Clean & Simple execution of core-cli SOFA pipeline
Provide some UX and verification that provides visibility in GH Actions.
No complex path detection, minimal TOML parsing.
"""

__version__ = "0.2.0"

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import typer

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

console = Console()
app = typer.Typer(help=f"SOFA Pipeline Clean v{__version__}")

class StageResult:
    def __init__(self, name: str, success: bool, duration: float, message: str = ""):
        self.name = name
        self.success = success
        self.duration = duration
        self.message = message

def check_environment() -> bool:
    """Check that we're in the right environment"""
    if not Path("bin").exists() or not Path("config").exists():
        console.print("❌ Must run from repo root or processing folder (needs bin/ and config/)", style="red")
        return False
        
    # Create necessary directories
    Path("data/resources").mkdir(parents=True, exist_ok=True)
    Path("data/models").mkdir(parents=True, exist_ok=True)
    Path("data/cache").mkdir(parents=True, exist_ok=True) 
    Path("v1").mkdir(parents=True, exist_ok=True)
    Path("v2").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    
    return True

def run_binary_command(cmd: List[str], stage_name: str, timeout: int = 600) -> StageResult:
    """Run a binary command and return result"""
    start_time = datetime.now()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        duration = (datetime.now() - start_time).total_seconds()
        
        # Show command output for transparency (last 300 chars to keep it readable)
        if result.stdout:
            # Clean up and show relevant output only
            clean_output = result.stdout.strip()
            if len(clean_output) > 300:
                clean_output = "..." + clean_output[-300:]
            console.print(f"[dim]stdout: {clean_output}[/dim]")
        if result.stderr:
            console.print(f"[red]stderr: {result.stderr[-300:]}[/red]")
        
        if result.returncode == 0:
            return StageResult(stage_name, True, duration, "Completed successfully")
        else:
            error_msg = f"Exit code {result.returncode}"
            if result.stderr:
                error_msg += f": {result.stderr[:300]}"
            return StageResult(stage_name, False, duration, error_msg)
            
    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start_time).total_seconds()
        return StageResult(stage_name, False, duration, f"Timed out after {timeout}s")
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        return StageResult(stage_name, False, duration, str(e))

def run_gather() -> StageResult:
    """Run gather stage"""
    console.rule("Gather")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Gathering all data sources...", total=1)
        
        cmd = ["./bin/sofa-gather", "all", "--continue-on-error"]
        result = run_binary_command(cmd, "gather")
        
        progress.advance(task)
    
    # Display results table
    if result.success:
        table = Table(title="Gather Results")
        table.add_column("File", style="cyan")
        table.add_column("Status", style="green")
        
        # Check expected files
        expected_files = [
            "kev_catalog.json", "gdmf_cached.json", "ipsw.json",
            "apple_beta_feed.json", "uma_catalog.json", "xprotect.json"
        ]
        
        table.add_row("all_sources", "✅")
        for file_name in expected_files:
            file_path = Path("data/resources") / file_name
            status = "✅" if file_path.exists() else "❌"
            table.add_row(file_name, status)
            
        console.print(table)
    
    return result

def run_fetch() -> StageResult:
    """Run fetch stage"""
    console.rule("Fetch")
    
    with console.status("[bold green]Fetching Apple security pages..."):
        cmd = [
            "./bin/sofa-fetch",
            "--kev-file", "data/resources/kev_catalog.json",
            "--preserve-html"
        ]
        
        result = run_binary_command(cmd, "fetch")
        
        if result.success:
            # Count releases
            releases_file = Path("data/resources/apple_security_releases.json")
            if releases_file.exists():
                with open(releases_file) as f:
                    data = json.load(f)
                    release_count = len(data.get("releases", []))
                    console.print(f"✅ Fetched {release_count} releases", style="green")
    
    return result


def run_bulletin() -> StageResult:
    """Generate bulletin data"""
    console.rule("[bold magenta]Bulletin Generation")

    with console.status("[bold magenta]Generating bulletin data..."):
        cmd = [
            "./bin/sofa-build", "bulletin",
            "-i", "data/resources",
            "-b", "data/resources/bulletin_data.json"
        ]

        result = run_binary_command(cmd, "bulletin", 60)

        if result.success and Path("data/resources/bulletin_data.json").exists():
            size = Path("data/resources/bulletin_data.json").stat().st_size
            console.print(f"✅ Bulletin generated ({size:,} bytes)", style="green")

            # Show summary if possible
            try:
                with open("data/resources/bulletin_data.json") as f:
                    bulletin = json.load(f)

                if "latest_releases" in bulletin:
                    table = Table(title="Latest Releases")
                    table.add_column("OS", style="cyan")
                    table.add_column("Version", style="yellow")
                    table.add_column("CVEs Fixed", style="green")
                    table.add_column("Exploited", style="red")

                    for os_name, info in bulletin["latest_releases"].items():
                        version = info.get("version", "")
                        if version:  # Only show if we have version data
                            cves_fixed = len(info.get("cves_fixed", []))
                            exploited = info.get("actively_exploited_count", 0)

                            table.add_row(
                                os_name.upper(),
                                version,
                                str(cves_fixed),
                                str(exploited)
                            )

                    if table.rows:  # Only show table if we have data
                        console.print(table)
                    else:
                        console.print("📋 No latest release data available yet", style="yellow")
            except:
                pass  # Skip table if bulletin format is different

    # Additional step: Generate bulletin from v2 feeds to ensure latest data
    if result.success and Path("v2").exists():
        console.print("🔄 Updating bulletin with v2 feeds data...", style="cyan")
        with console.status("[bold cyan]Updating bulletin from v2 feeds..."):
            v2_cmd = [
                "./bin/sofa-build", "bulletin",
                "--feeds-dir", "."
            ]

            v2_result = run_binary_command(v2_cmd, "bulletin-v2", 60)

            if v2_result.success:
                console.print("✅ Bulletin updated with v2 feeds data", style="green")
            else:
                console.print("⚠️ Failed to update bulletin with v2 feeds, using original", style="yellow")

    return result

def run_rss() -> StageResult:
    """Generate RSS feed"""
    console.rule("[bold purple]RSS Feed Generation")
    
    with console.status("[bold purple]Generating RSS feed..."):
        cmd = [
            "./scripts/generate_rss.py",
            "--output", "v1/rss_feed.xml",
            "--data-dir", "data/resources", 
            "--include-xprotect",
            "--include-beta",
            "--verbose"
        ]
        
        result = run_binary_command(cmd, "rss", 60)
        
        # Check for RSS feed in v1/ directory
        rss_file = Path("v1/rss_feed.xml")
        
        if result.success and rss_file.exists():
            size = rss_file.stat().st_size
            console.print(f"✅ RSS feed generated ({size:,} bytes) in v1/", style="green")
    
    return result

def run_transform_links() -> StageResult:
    """Transform essential_links.toml to JSON"""
    console.rule("[bold purple]Transform Essential Links")
    
    with console.status("[bold purple]Transforming essential_links.toml to JSON..."):
        cmd = ["./scripts/transform_essential_links.py"]
        result = run_binary_command(cmd, "transform_links", 30)
        
        # Check for generated JSON file
        json_file = Path("data/resources/essential_links.json")
        
        if result.success and json_file.exists():
            size = json_file.stat().st_size
            console.print(f"✅ Essential links JSON generated ({size:,} bytes)", style="green")
            
            # Show content summary
            try:
                import json
                with open(json_file) as f:
                    data = json.load(f)
                platforms = [k for k in data.keys() if not k.startswith("_")]
                general_resources = len(data.get("_general_resources", []))
                console.print(f"   📱 Platforms: {', '.join(platforms)}", style="cyan")
                console.print(f"   🔗 General resources: {general_resources}", style="cyan")
            except:
                pass  # Skip summary if JSON parsing fails
    
    return result


def verify_results() -> None:
    """Display comprehensive results verification"""
    console.rule("Verify")
    
    tree = Tree("📁 Pipeline Output")
    data_tree = tree.add("📂 data/")
    resources_tree = data_tree.add("📂 resources/")
    
    # Check gathered files with validation
    gather_files = [
        ("kev_catalog.json", "KEV entries", ".vulnerabilities | length"),
        ("gdmf_cached.json", "GDMF entries", ".PublicAssetSets // {} | keys | length"),
        ("ipsw.json", "IPSW devices", "keys | length"), 
        ("apple_beta_feed.json", "Beta releases", ".items | length"),
        ("uma_catalog.json", "UMA entries", "keys | length"),
        ("xprotect.json", "XProtect data", "keys | length")
    ]
    
    for file_name, description, jq_query in gather_files:
        path = Path("data/resources") / file_name
        if path.exists():
            size = path.stat().st_size
            
            # Try jq validation
            try:
                result = subprocess.run(
                    ["jq", "-r", jq_query, str(path)],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0 and result.stdout.strip().isdigit():
                    count = int(result.stdout.strip())
                    resources_tree.add(f"✅ {file_name} ({size:,} bytes, {count:,} {description})")
                else:
                    resources_tree.add(f"✅ {file_name} ({size:,} bytes)")
            except:
                resources_tree.add(f"✅ {file_name} ({size:,} bytes)")
        else:
            resources_tree.add(f"❌ {file_name}")
    
    # Check fetch results
    fetch_file = Path("data/resources/apple_security_releases.json")
    if fetch_file.exists():
        size = fetch_file.stat().st_size
        resources_tree.add(f"✅ apple_security_releases.json ({size:,} bytes)")
    else:
        resources_tree.add("❌ apple_security_releases.json")
    
    # Check v1/ and v2/ directories in root (not data/feeds)
    v1_tree = tree.add("📂 v1/")
    v2_tree = tree.add("📂 v2/")
    
    for version, version_tree in [("v1", v1_tree), ("v2", v2_tree)]:
        for product in ["safari", "ios", "macos", "tvos", "watchos", "visionos"]:
            feed_file = Path(f"{version}/{product}_data_feed.json")
            
            if feed_file.exists():
                size = feed_file.stat().st_size
                version_tree.add(f"✅ {product}_data_feed.json ({size:,} bytes)")
            else:
                version_tree.add(f"❌ {product}_data_feed.json")
        
        # Check for RSS feed in v1
        if version == "v1":
            rss_file = Path("v1/rss_feed.xml")
            if rss_file.exists():
                size = rss_file.stat().st_size
                version_tree.add(f"✅ rss_feed.xml ({size:,} bytes)")
            else:
                version_tree.add("❌ rss_feed.xml")
    
    console.print(tree)

@app.command()
def run(
    stage: str = typer.Argument("all", help="Stage to run: gather, fetch, build, rss, transform_links, all")
):
    """Run SOFA pipeline with beautiful UX and simple implementation"""
    
    console.print(Panel.fit(
        "[bold blue]SOFA Pipeline Clean[/bold blue]\n"
        "[dim]gather → fetch → build → rss[/dim]",
        border_style="blue"
    ))
    
    # Environment check
    if not check_environment():
        sys.exit(1)
    
    # Pre-flight setup
    console.rule("[bold yellow]Pre-flight Setup")
    console.print("✅ Using embedded defaults in binaries", style="green")
    console.print(f"🔍 Detected paths: bin={Path('bin').resolve()}, config={Path('config').resolve()}, data={Path('data').resolve()}", style="cyan")
    console.print("✅ Directories created", style="green")
    console.print("✅ Binaries used in place", style="green")
    
    # Configuration validation
    console.rule("[bold yellow]Configuration Validation")
    console.print("🔍 Validating configuration...")
    
    # Check binaries
    binaries = ["sofa-gather", "sofa-fetch", "sofa-build", "sofa-cve"]
    missing_binaries = []
    
    for binary in binaries:
        if not Path(f"bin/{binary}").exists():
            missing_binaries.append(binary)
    
    if missing_binaries:
        console.print(f"❌ Missing binaries: {', '.join(missing_binaries)}", style="red")
        sys.exit(1)
    
    console.print("✅ Configuration validated", style="green")
    console.print("✅ Configuration ready", style="green")
    
    # Run stages
    results = []
    
    if stage == "all":
        stages = ["gather", "fetch", "build", "rss", "transform_links"]
    else:
        stages = [stage]
    
    for stage_name in stages:
        if stage_name == "gather":
            result = run_gather()
        elif stage_name == "fetch":
            result = run_fetch()
        elif stage_name == "build":
            # Here we build all feeds with legacy mode in single call
            console.rule("[bold blue]Build All Feeds")
            console.print("🔧 Building all feeds (v1 + v2) with legacy mode...")
            
            cmd = ["./bin/sofa-build", "all", "--legacy"]
            console.print(f"🚀 Running: {' '.join(cmd)}")
            result = run_binary_command(cmd, "build_all", 600)
            
            if result.success:
                console.print("✅ All feeds built successfully", style="green")
                
                # Show build results for both versions
                table = Table(title="Build Results")
                table.add_column("Version", style="cyan")
                table.add_column("Product", style="blue")
                table.add_column("Status", style="green")
                
                for version in ["v1", "v2"]:
                    for product in ["safari", "ios", "macos", "tvos", "watchos", "visionos"]:
                        feed_file = Path(f"{version}/{product}_data_feed.json")
                        status = "✅" if feed_file.exists() else "❌"
                        table.add_row(version, product, status)
                
                console.print(table)
                
            else:
                console.print(f"❌ Build failed: {result.message}", style="red")
                
            results.append(result)
            continue
        elif stage_name == "bulletin":
            result = run_bulletin()
        elif stage_name == "rss":
            result = run_rss()
        elif stage_name == "transform_links":
            result = run_transform_links()
        else:
            console.print(f"❌ Unknown stage: {stage_name}", style="red")
            continue
            
        results.append(result)
        
        if not result.success and stage != "all":
            console.print(f"❌ Stage {stage_name} failed, stopping", style="red")
            sys.exit(1)
    
    # Verify results
    verify_results()
    
    # Summary
    console.rule("[bold green]Summary")
    
    total_duration = sum(r.duration for r in results)
    success_count = sum(1 for r in results if r.success)
    
    summary_table = Table(title="Execution Summary")
    summary_table.add_column("Stage", style="cyan")
    summary_table.add_column("Status", style="green")
    summary_table.add_column("Duration", style="yellow")
    
    for result in results:
        status = "✅ Success" if result.success else "❌ Failed"
        summary_table.add_row(result.name, status, f"{result.duration:.1f}s")
    
    console.print(summary_table)
    
    # Show errors for failed stages
    failed_results = [r for r in results if not r.success]
    if failed_results:
        console.rule("[bold red]Failed Stage Details")
        for result in failed_results:
            console.print(f"[bold red]{result.name} failed:[/bold red]")
            console.print(f"  • {result.message}", style="red")
    
    # Final status
    if success_count == len(results):
        console.print(f"\n✅ [bold green]Pipeline completed successfully in {total_duration:.1f}s[/bold green]")
    else:
        console.print(f"\n⚠️ [bold yellow]Pipeline completed with {len(results) - success_count} failures in {total_duration:.1f}s[/bold yellow]")

@app.command()
def check():
    """Check environment and show current state"""
    console.print("🔍 Environment Check")
    console.print("==================")
    
    console.print(f"📍 Working directory: {Path.cwd()}")
    
    # Check structure
    structure_items = [
        ("bin/", "Binary directory"),
        ("config/", "Configuration directory"), 
        ("data/resources/", "Data resources"),
        ("v1/", "v1 feeds"),
        ("v2/", "v2 feeds"),
        ("scripts/", "Scripts directory")
    ]
    
    for path_str, description in structure_items:
        path = Path(path_str)
        if path.exists():
            if path.is_dir():
                file_count = len(list(path.iterdir()))
                console.print(f"  ✅ {path_str} ({file_count} items)")
            else:
                console.print(f"  ✅ {path_str}")
        else:
            console.print(f"  ❌ {path_str} - {description}")

if __name__ == "__main__":
    app()