import argparse
import threading
import time
import schedule
from weather_collector import main as collector_main
from app import app

def run_collector_once():
    """Run the weather collector once"""
    print("Running weather collector...")
    collector_main()
    print("Weather collector completed")

def run_collector_scheduled(interval_hours=1):
    """Run the weather collector on a schedule"""
    print(f"Starting scheduled weather collector (every {interval_hours} hours)")
    
    # Run once immediately
    run_collector_once()
    
    # Schedule future runs
    schedule.every(interval_hours).hours.do(run_collector_once)
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def run_web_app(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask web application"""
    print(f"Starting web application on {host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Tracker Application")
    parser.add_argument('--collector', action='store_true', help='Run the weather collector once')
    parser.add_argument('--schedule', type=int, help='Run the collector on a schedule (specify hours)')
    parser.add_argument('--web', action='store_true', help='Run the web application')
    parser.add_argument('--host', default='0.0.0.0', help='Host for the web application')
    parser.add_argument('--port', type=int, default=5000, help='Port for the web application')
    parser.add_argument('--debug', action='store_true', help='Run the web application in debug mode')
    
    args = parser.parse_args()
    
    # Default behavior: run both collector once and web app
    if not (args.collector or args.schedule or args.web):
        print("No specific mode selected, running both collector and web app")
        # Run collector in a separate thread
        collector_thread = threading.Thread(target=run_collector_once)
        collector_thread.daemon = True
        collector_thread.start()
        
        # Run web app in the main thread
        run_web_app(args.host, args.port, args.debug)
    else:
        # Run collector once if requested
        if args.collector:
            run_collector_once()
        
        # Run collector on schedule if requested
        if args.schedule:
            if args.web:
                # Run scheduled collector in a separate thread
                collector_thread = threading.Thread(target=run_collector_scheduled, args=(args.schedule,))
                collector_thread.daemon = True
                collector_thread.start()
            else:
                # Run scheduled collector in the main thread
                run_collector_scheduled(args.schedule)
        
        # Run web app if requested
        if args.web:
            run_web_app(args.host, args.port, args.debug) 