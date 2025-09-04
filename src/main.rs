mod cli;
mod constants;
mod files;
mod output;
mod process;

use cli::parse_args;
use files::collect_files;
use output::write_output;
use process::process_files;

fn main() {
  let args = parse_args();

  let files = match collect_files(&args.inputs) {
    Ok(f) => f,
    Err(e) => {
      eprintln!("Error collecting files: {}", e);
      std::process::exit(1);
    }
  };

  // Process files
  let (headers, impls, sys_includes) = process_files(&files);

  // Write output header
  if let Err(e) = write_output(&args.out, &args.impl_macro, headers, impls, sys_includes) {
    eprintln!("Error writing output file: {}", e);
    std::process::exit(1);
  }

  println!("Successfully generated `{}` file", args.out.display());
}
