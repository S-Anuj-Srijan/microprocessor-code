use std::process::{Command, Stdio};
use std::io::Write;

pub fn runpythonfile(inputpath: &str) {
    let mut child = Command::new("python")
        .arg(inputpath)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("Failed to start Python script");

    if let Some(stdin) = child.stdin.as_mut() {
        stdin
            .write_all(b"input\n")
            .expect("Failed to write to Python stdin");
    }

    let output = child
        .wait_with_output()
        .expect("Failed to read Python output");

    let python_output = String::from_utf8_lossy(&output.stdout);
    println!("Output from Python:\n{}", python_output);
}
