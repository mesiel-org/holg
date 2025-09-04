use crate::constants::FILES_EXTENSIONS;
use std::fs;
use std::io;
use std::path::PathBuf;

/// Recursively collect all files from the given roots
/// Returns a list of file paths
pub fn collect_files(roots: &[PathBuf]) -> io::Result<Vec<PathBuf>> {
  let mut files = Vec::new();

  for root in roots {
    if root.is_file() {
      files.push(root.clone());
    } else if root.is_dir() {
      for entry in fs::read_dir(root)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_dir() {
          files.extend(collect_files(&[path])?);
        } else if let Some(ext) = path.extension() {
          if let Some(ext_str) = ext.to_str() {
            if FILES_EXTENSIONS.contains(&ext_str) {
              files.push(path);
            }
          }
        }
      }
    }
  }

  Ok(files)
}
