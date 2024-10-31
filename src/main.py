import argparse
from src.CLI import CLI
from src.GUI import GUI

def main():
    parser = argparse.ArgumentParser(description="Vulnerability Scanner Tool")
    parser.add_argument("-m", "--mode", choices=["cli", "gui"], default="cli",
                        help="Choose 'cli' for command-line interface or 'gui' for graphical interface")
    args = parser.parse_args()

    if args.mode == "cli":
        cli = CLI()
        cli.run()
    elif args.mode == "gui":
        gui = GUI()
        gui.run()

if __name__ == "__main__":
    main()
