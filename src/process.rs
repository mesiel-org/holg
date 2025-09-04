use rayon::prelude::*;
use std::collections::HashSet;
use std::fs;
use std::path::PathBuf;

/// Strip system includes and unnecessary directives from file content
/// Returns cleaned string
pub fn strip_include_and_define(content: &str, sys_includes: &mut HashSet<String>) -> String {
  let mut out = String::new();

  for line in content.lines() {
    let l = line.trim();

    if l.starts_with("#include \"") {
      continue;
    }
    if l.starts_with("#include <") {
      sys_includes.insert(l.to_string());
      continue;
    }
    if l.starts_with("#pragma once")
      || l.starts_with("#ifndef")
      || l.starts_with("#define")
      || l.starts_with("#endif")
    {
      continue;
    }
    if l.is_empty() {
      continue;
    }

    out.push_str(line);
    out.push('\n');
  }

  out
}

/// Process files in parallel
/// Return tuple: `(headers, impls, system_includes)`
pub fn process_files(
  files: &[PathBuf],
) -> (
  Vec<(PathBuf, String)>,
  Vec<(PathBuf, String)>,
  HashSet<String>,
) {
  let sys_includes = std::sync::Mutex::new(HashSet::new());

  let results: Vec<_> = files
    .par_iter()
    .map(|file| {
      let content = fs::read_to_string(file).expect("Failed to read file");
      let mut local_sys_includes = HashSet::new();
      let cleaned = strip_include_and_define(&content, &mut local_sys_includes);
      (file.clone(), cleaned, local_sys_includes)
    })
    .collect();

  let mut headers = Vec::new();
  let mut impls = Vec::new();

  for (path, cleaned, local_sys_includes) in results {
    sys_includes.lock().unwrap().extend(local_sys_includes);

    if path.extension().map(|e| e == "h").unwrap_or(false) {
      headers.push((path, cleaned));
    } else {
      impls.push((path, cleaned));
    }
  }

  (headers, impls, sys_includes.into_inner().unwrap())
}
