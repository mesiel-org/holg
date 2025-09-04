use std::env;
use std::path::PathBuf;

/// CLI arguments
pub struct Args {
  pub inputs: Vec<PathBuf>,
  pub out: PathBuf,
  pub impl_macro: String,
}

const VERSION: &str = env!("CARGO_PKG_VERSION");
const HELP_FILE: &str = include_str!("help.txt");

/// Print usage information
fn print_usage() {
  println!("{}", HELP_FILE);
}

/// Parse command-line arguments
/// Exits if inputs are invalid or `--help/-h` / `--version/-v` is requested.
pub fn parse_args() -> Args {
  let mut inputs = Vec::new();
  let mut out = PathBuf::from("holg.h");
  let mut impl_macro = "MESIEL_HOLG".to_string();

  let args: Vec<String> = env::args().skip(1).collect();
  let mut i = 0;

  while i < args.len() {
    match args[i].as_str() {
      "-h" | "--help" => {
        print_usage();
        std::process::exit(0);
      }
      "-v" | "--version" => {
        println!("holg version {}", VERSION);
        std::process::exit(0);
      }
      "-o" | "--out" => {
        i += 1;
        if i >= args.len() {
          eprintln!("Error: expected value after {}", args[i - 1]);
          print_usage();
          std::process::exit(1);
        }
        out = PathBuf::from(&args[i]);
      }
      "-i" | "--impl" => {
        i += 1;
        if i >= args.len() {
          eprintln!("Error: expected value after {}", args[i - 1]);
          print_usage();
          std::process::exit(1);
        }
        impl_macro = args[i].clone();
      }
      s => {
        inputs.push(PathBuf::from(s));
      }
    }
    i += 1;
  }

  if inputs.is_empty() {
    eprintln!("Error: No input files or directories provided.");
    print_usage();
    std::process::exit(1);
  }

  Args {
    inputs,
    out,
    impl_macro,
  }
}
