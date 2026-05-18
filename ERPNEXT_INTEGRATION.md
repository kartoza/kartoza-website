# ERPNext Training Integration

This document explains how the training schedule integrates with ERPNext.

## ✅ What's Installed

The nix shell now includes:
- `python3` - Python interpreter.
- `python3Packages.requests` - For ERPNext API calls.
- `python3Packages.pyyaml` - For YAML file generation.

## 🔧 Setup Instructions

### 1. Get ERPNext API Credentials

In your ERPNext instance:

1. **Go to User Menu → API Access**
2. **Generate Keys** for the API user
3. **Copy the API Key and API Secret**

Or use the API endpoint:
```bash
curl -X POST "https://erp.kartoza.com/api/method/frappe.core.doctype.user.user.generate_keys" \
  -H "Content-Type: application/json" \
  -d '{"user": "your-email@kartoza.com"}'
```

### 2. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Add:
```bash
ERPNEXT_API_URL=https://erp.kartoza.com
ERPNEXT_API_KEY=your_api_key_here
ERPNEXT_API_SECRET=your_api_secret_here
```

### 3. Customize the Sync Script

Edit `scripts/sync-training-from-erpnext.py` to match your ERPNext setup:

**A. Update DocType Names**

In `fetch_training_courses()`:
```python
# Change "Item" to your training course DocType
response = self.session.get(
    f"{self.api_url}/api/resource/YourTrainingDocType",
    params={
        'filters': json.dumps([
            ["disabled", "=", 0]
        ]),
        # Add your custom fields here
    }
)
```

**B. Update Session Fetching**

In `fetch_training_sessions()`:
```python
# Change "Event" to how you track training sessions
# Could be: Event, Project, Custom DocType
response = self.session.get(
    f"{self.api_url}/api/resource/YourSessionDocType",
    # Customize filters and fields
)
```

**C. Update Field Mappings**

In `_extract_course_slug()`, add your course mappings:
```python
course_map = {
    'your course name in erpnext': 'hugo-slug',
    'qgis introduction': 'qgis-introduction',
    # ... add all your courses
}
```

## 🚀 Usage

### Manual Sync

```bash
# Enter nix shell
nix develop

# Sync with default cache (6 hours)
./scripts/sync-training-from-erpnext.py

# Force fresh data
./scripts/sync-training-from-erpnext.py --force

# Dry run (test without writing)
./scripts/sync-training-from-erpnext.py --dry-run

# Custom cache TTL
./scripts/sync-training-from-erpnext.py --cache-ttl 12
```

### Automatic Sync with Build

```bash
# Development server (syncs automatically)
nix develop --command ./scripts/dev-server.sh

# Production build (syncs automatically)
nix develop --command ./scripts/build.sh
```

### Pre-build Only

```bash
# Run just the pre-build sync
nix develop --command ./scripts/pre-build.sh
```

## 📁 How It Works

### Data Flow

```
┌─────────────┐
│   ERPNext   │
│  (Courses,  │
│  Sessions,  │
│  Pricing)   │
└──────┬──────┘
       │
       │ API Call
       │
       ▼
┌──────────────────────────┐
│  sync-training-from-     │
│  erpnext.py              │
│  - Fetches data          │
│  - Transforms format     │
│  - Handles caching       │
└──────┬───────────────────┘
       │
       │ Writes YAML
       │
       ▼
┌──────────────────────────┐
│  data/                   │
│  training_schedule.yml   │
└──────┬───────────────────┘
       │
       │ Hugo reads
       │
       ▼
┌──────────────────────────┐
│  Training Course Pages   │
│  - Booking widget        │
│  - Session cards         │
│  - Pricing calculator    │
└──────────────────────────┘
```

### Caching Strategy

**Development Mode** (HUGO_ENV != production):
- Cache TTL: 6 hours
- Reduces API calls during frequent rebuilds
- Allows offline development

**Production Mode** (HUGO_ENV=production):
- Cache TTL: 1 hour
- Fresher data for production builds
- Still provides fallback if API is down

**Cache Location**: `.cache/training_schedule_cache.json`

**Fallback Behaviour**:
1. Try to fetch from ERPNext
2. If fails, use cache (any age)
3. If no cache, keep existing YAML file
4. Build continues regardless

## 🧪 Testing

### Test Without ERPNext (Current State)

```bash
# The scripts work fine without ERPNext credentials
# They fall back to the manually-maintained YAML file
nix develop --command ./scripts/dev-server.sh
```

### Test With Mock Data

Create a test script:
```bash
# Create test credentials
export ERPNEXT_API_URL=https://erp.kartoza.com
export ERPNEXT_API_KEY=test_key
export ERPNEXT_API_SECRET=test_secret

# Run sync (will fail but show the flow)
./scripts/sync-training-from-erpnext.py --dry-run
```

## 📊 ERPNext Data Structure Expected

### Training Courses (Item or Custom DocType)

```json
{
  "name": "ITEM-001",
  "item_code": "QGIS-INTRO",
  "item_name": "QGIS Introduction",
  "description": "Learn QGIS basics...",
  "item_group": "Training Courses",
  "disabled": 0
}
```

### Training Sessions (Event or Custom DocType)

```json
{
  "name": "EVENT-001",
  "subject": "QGIS Introduction - Cape Town",
  "starts_on": "2024-04-15 09:00:00",
  "ends_on": "2024-04-17 17:00:00",
  "event_category": "Training",
  "event_type": "Public",
  "description": "Cape Town venue, Tim Sutton instructor",
  "event_participants": [
    {"reference_docname": "Tim Sutton"}
  ]
}
```

### Pricing (Item Price)

```json
{
  "item_code": "QGIS-INTRO",
  "price_list": "Standard Selling",
  "price_list_rate": 7500,
  "currency": "ZAR"
}
```

## 🔍 Troubleshooting

### "No module named 'yaml'"

The nix shell has been updated, but you need to reload:
```bash
exit  # Exit current shell
nix develop  # Enter fresh shell
```

### "ERPNext credentials not found"

1. Check `.env` file exists
2. Verify credentials are correct
3. Load environment variables:
   ```bash
   set -a; source .env; set +a
   ```

### API Connection Fails

Test the connection:
```bash
curl -X GET "https://erp.kartoza.com/api/resource/Item" \
  -H "Authorization: token YOUR_KEY:YOUR_SECRET"
```

Check:
- API user has correct permissions
- IP whitelisting (if enabled)
- ERPNext instance is accessible

### Sync Fails During Build

The build won't fail! It will:
1. Warn about sync failure
2. Use cached data
3. Fall back to existing YAML
4. Continue building

To debug:
```bash
# Run sync manually to see errors
./scripts/sync-training-from-erpnext.py --force
```

### Cache Issues

Clear cache and force refresh:
```bash
rm -rf .cache/
./scripts/sync-training-from-erpnext.py --force
```

## 🎯 Next Steps

### Immediate (Can Use Now)

✅ Training booking flow is working with manual YAML
✅ Beautiful session cards and pricing
✅ Scripts are ready for ERPNext integration

### To Enable ERPNext Sync

1. **Get API credentials** from your ERPNext instance
2. **Configure `.env`** with credentials
3. **Customize the sync script** to match your ERPNext setup:
   - Update DocType names
   - Map field names
   - Adjust course slug mappings
4. **Test the sync**: `./scripts/sync-training-from-erpnext.py --dry-run`
5. **Use integrated build**: `./scripts/dev-server.sh`

### Future Enhancements

- **Real-time availability checking** via API
- **Booking submission** to ERPNext
- **Email confirmations** from ERPNext workflow
- **Payment integration** with ERPNext Payment Gateway
- **Automatic capacity tracking** from participant count

## 📞 Support

The sync script includes helpful error messages and fallback behaviour. If you need help customizing it for your specific ERPNext setup, the script is well-documented with comments explaining each section.

Current maintainer: Can be customized for your specific ERPNext DocType structure.
