# ParkNload Simple Driver Webapp

A simple and focused web application for drivers to access their delivery routes and track their location to the delivery point.

## Features

### 🔐 **Simple Access**
- OTP/code-based authentication
- No complex login system
- Quick access to delivery information

### 🗺️ **Route Map**
- Interactive Google Maps integration
- Shows current location to delivery point
- Real-time route calculation
- Distance and time estimates

### 📍 **Location Tracking**
- GPS location access
- Start/stop tracking functionality
- Location updates every 30 seconds
- Manual location refresh option

### 📦 **Delivery Management**
- View delivery details (pickup, delivery, customer)
- Mark deliveries as completed
- Simple status tracking

## Getting Started

### Prerequisites
- Python 3.7+
- Flask web framework
- Google Maps API key (for map functionality)
- Modern web browser with geolocation support

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd ParkNload
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Maps API**:
   - Get a Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Replace `YOUR_GOOGLE_MAPS_API_KEY` in `app/templates/driver/delivery.html`

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Access the driver webapp**:
   Open your browser and navigate to: `http://localhost:5050/drivers/`

## Usage Guide

### Step 1: Access the Webapp
- Navigate to `/drivers/`
- You'll see a simple OTP entry form

### Step 2: Enter Delivery Code
- **Test Code**: Use `1234` for testing
- Enter your unique delivery code
- Click "Access Delivery"

### Step 3: View Delivery Route
- See your delivery details
- View the interactive map
- Start location tracking

### Step 4: Track Delivery
- Click "Start Tracking" to begin location updates
- View real-time route from your location to delivery point
- Mark delivery as completed when finished

## How It Works

### OTP Verification
- Simple code-based access (currently hardcoded as "1234")
- Can be enhanced to use database-stored codes
- Session-based authentication

### Location Tracking
- Uses browser's Geolocation API
- Updates location every 30 seconds when tracking is active
- Sends location data to server for logging

### Route Calculation
- Google Maps Directions API
- Shows optimal driving route
- Calculates distance and estimated time

## Configuration

### Google Maps API
1. Get API key from Google Cloud Console
2. Enable Maps JavaScript API and Directions API
3. Replace placeholder in `delivery.html`:
   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_ACTUAL_API_KEY&libraries=geometry"></script>
   ```

### Customizing Delivery Data
Modify the delivery data in `app/routes/drivers.py`:
```python
delivery = {
    'pickup': 'Your Pickup Address',
    'delivery': 'Your Delivery Address',
    'customer': 'Customer Name',
    'phone': 'Customer Phone'
}
```

## API Endpoints

### Simple API Structure
- `GET /drivers/` - OTP entry page
- `POST /drivers/verify` - Verify OTP and get delivery
- `GET /drivers/delivery` - Delivery tracking page
- `POST /drivers/api/location` - Update driver location

## Browser Compatibility

The webapp requires a modern browser with geolocation support:

- ✅ **Chrome** (recommended)
- ✅ **Firefox**
- ✅ **Safari** (iOS 13+)
- ✅ **Edge**
- ❌ **Internet Explorer** (not supported)

## Mobile Usage

The webapp is fully responsive and optimized for mobile:

- Touch-friendly interface
- Mobile-optimized map display
- Responsive design for all screen sizes

## Security Features

- **HTTPS Recommended**: Use HTTPS in production for secure location data
- **Input Validation**: OTP verification with proper error handling
- **Session Management**: Simple session-based access control

## Customization

### Adding Real OTP System
Replace the hardcoded OTP in `verify_otp()` function:
```python
# Instead of: if otp == "1234":
# Use database lookup or external service
driver = Driver.query.filter_by(otp=otp).first()
if driver:
    # Grant access
```

### Adding Multiple Deliveries
Modify the verification to return different deliveries based on OTP:
```python
deliveries = {
    "1234": {"pickup": "Location A", "delivery": "Location B"},
    "5678": {"pickup": "Location C", "delivery": "Location D"}
}
```

## Troubleshooting

### Common Issues

1. **Map Not Loading**:
   - Check Google Maps API key
   - Verify API is enabled in Google Cloud Console
   - Check browser console for errors

2. **Location Not Working**:
   - Check browser permissions
   - Ensure HTTPS is used (required for geolocation)
   - Try refreshing the page

3. **OTP Not Working**:
   - Use test code "1234"
   - Check browser console for errors
   - Verify server is running

### Debug Mode
Enable debug mode for detailed error messages:
```python
# In main.py
app.run(debug=True, port=5050)
```

## Project Structure

```
app/
├── routes/
│   └── drivers.py          # Driver routes (OTP + delivery)
├── static/
│   └── css/
│       └── driver.css      # Simple styling
└── templates/
    └── driver/             # Driver templates
        ├── index.html      # OTP entry page
        └── delivery.html   # Delivery tracking page
```

## Deployment

### Production Considerations

1. **HTTPS**: Enable SSL/TLS for secure location data
2. **Google Maps API**: Set up proper API key restrictions
3. **Database**: Implement proper OTP storage system
4. **Monitoring**: Add logging for delivery tracking

### Simple Deployment
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5050 main:app
```

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review browser console for errors
3. Verify Google Maps API key is correct
4. Check server logs for backend errors

## License

This project is part of the ParkNload logistics platform.

---

**Note**: This is a simplified driver webapp focused on essential delivery tracking functionality. The OTP system can be enhanced with database integration and real authentication as needed.
