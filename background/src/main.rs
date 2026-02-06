use std::thread;

mod pythonspawn;
use pythonspawn::runpythonfile;

fn main() {
    let handle_model = thread::spawn(|| {
        runpythonfile("utils/model.py");
    });

    let handle_logging = thread::spawn(|| {
        runpythonfile("utils/logging.py");
    });

    // Wait for both threads to finish
    handle_model.join().expect("Model thread panicked");
    handle_logging.join().expect("Logging thread panicked");
}
