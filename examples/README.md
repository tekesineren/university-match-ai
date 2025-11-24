# Example Usage

## Sample Profile

See `sample_profile.json` for an example user profile structure.

## Running Analysis

```bash
# From project root
cd backend
python app.py

# In another terminal, use the API
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d @../examples/sample_profile.json
```

## Expected Output

The API will return matched universities categorized by match score:
- High Match: 70+ points
- Medium Match: 50-70 points
- Low Match: 30-50 points
- Extra Options: <30 points

