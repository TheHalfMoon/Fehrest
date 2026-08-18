//! Fehrest Phase T CLI entry point.

use std::process::ExitCode;

fn main() -> ExitCode {
    let argv: Vec<String> = std::env::args().skip(1).collect();
    match fehrest::cli::run(&argv) {
        Ok(code) => ExitCode::from(code as u8),
        Err(e) => {
            // Explicit failure. No fail-open fallback anywhere on this path.
            eprintln!("error: {e}");
            ExitCode::from(1)
        }
    }
}
