from fastapi import FastAPI
from pydantic import BaseModel
from faker import Faker
import random
import time
import json
from datetime import datetime, timedelta
from typing import Optional, List

app = FastAPI()
fake = Faker()

# Scam-related categories - one per record
SCAM_CATEGORIES = [
    'Investment opportunity',
    'Double your money',
    'Get rich quick',
    'Guaranteed returns',
    'Risk-free investment',
    'Passive income',
    'Limited time offer',
    'High yield investment',
    'Crypto windfall',
    'Forex secrets',
    'IRS agent',
    'Police warrant',
    'Legal notice',
    'Government refund',
    'Social Security issue',
    'FBI alert',
    'Court summons',
    'Tax audit',
    'Arrest warrant',
    'Legal threat',
    'You\'ve won',
    'Claim your prize',
    'Lucky winner',
    'Free iPhone',
    'Scratch and win',
    'Contest winner',
    'Spin the wheel',
    'Free vacation',
    'Redeem reward',
    'Unclaimed funds',
    'Urgent payment',
    'Account suspended',
    'Confirm your identity',
    'Billing error',
    'Payment failed',
    'Wire transfer',
    'Bank verification',
    'Card declined',
    'Refund request',
    'Unauthorized access',
    'Your PC is infected',
    'Suspicious login attempt',
    'Account security alert',
    'Click to scan',
    'Update required',
    'Reset your password',
    'Apple ID locked',
    'Windows license expired',
    'Tech support needed',
    'System breach'
]

# Keyword to category mapping
KEYWORD_CATEGORY_MAPPING = {
    'investment': ['Investment opportunity', 'Double your money', 'Get rich quick', 'Guaranteed returns', 'Risk-free investment', 'High yield investment'],
    'money': ['Double your money', 'Get rich quick', 'Passive income', 'Guaranteed returns', 'Risk-free investment'],
    'crypto': ['Crypto windfall', 'Investment opportunity', 'High yield investment', 'Get rich quick', 'Double your money'],
    'forex': ['Forex secrets', 'Investment opportunity', 'High yield investment', 'Guaranteed returns', 'Risk-free investment'],
    'bitcoin': ['Crypto windfall', 'Investment opportunity', 'High yield investment', 'Get rich quick'],
    'profit': ['Double your money', 'Get rich quick', 'Guaranteed returns', 'Passive income', 'High yield investment'],
    'income': ['Passive income', 'Investment opportunity', 'Double your money', 'Get rich quick'],
    'winner': ['You\'ve won', 'Claim your prize', 'Lucky winner', 'Contest winner', 'Free iPhone'],
    'prize': ['Claim your prize', 'You\'ve won', 'Lucky winner', 'Contest winner', 'Scratch and win'],
    'lottery': ['You\'ve won', 'Lucky winner', 'Claim your prize', 'Contest winner', 'Scratch and win'],
    'free': ['Free iPhone', 'Free vacation', 'You\'ve won', 'Claim your prize', 'Spin the wheel'],
    'gift': ['Free iPhone', 'Free vacation', 'Claim your prize', 'You\'ve won', 'Redeem reward'],
    'urgent': ['Urgent payment', 'Account suspended', 'Limited time offer', 'Legal threat', 'Payment failed'],
    'suspended': ['Account suspended', 'Urgent payment', 'Confirm your identity', 'Unauthorized access', 'Account security alert'],
    'verify': ['Confirm your identity', 'Bank verification', 'Account security alert', 'Reset your password', 'Update required'],
    'security': ['Account security alert', 'Suspicious login attempt', 'Unauthorized access', 'Reset your password', 'System breach'],
    'police': ['Police warrant', 'FBI alert', 'Legal notice', 'Court summons', 'Arrest warrant'],
    'irs': ['IRS agent', 'Tax audit', 'Government refund', 'Legal notice', 'Court summons'],
    'government': ['Government refund', 'IRS agent', 'Social Security issue', 'Legal notice', 'FBI alert'],
    'refund': ['Government refund', 'Billing error', 'Refund request', 'Payment failed', 'Bank verification']
}

# Request body model
class AdSearchRequest(BaseModel):
    keyword: List[str]  # Changed to accept list of keywords
    category: Optional[bool] = None  # Filter category but default 'all'
    location: Optional[str] = "thailand"
    language: Optional[str] = "thai"
    advertiser: Optional[str] = "all"
    platform: Optional[str] = "all"
    media_type: Optional[str] = "all"
    status: Optional[str] = "all"
    start_date: Optional[str] = "June 18,2018"
    end_date: Optional[str] = "today"
    limit: Optional[int] = 1000

# Generate category based on keywords
def generate_keyword_based_category(keywords):
    # Collect all matching categories from all keywords
    all_matching_categories = []
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        
        # Find matching categories for this keyword
        matching_categories = []
        for key, categories in KEYWORD_CATEGORY_MAPPING.items():
            if key in keyword_lower or keyword_lower in key:
                matching_categories.extend(categories)
        
        # If no specific match found, check for partial matches
        if not matching_categories:
            for key, categories in KEYWORD_CATEGORY_MAPPING.items():
                if any(word in keyword_lower for word in key.split()) or any(word in key for word in keyword_lower.split()):
                    matching_categories.extend(categories)
        
        all_matching_categories.extend(matching_categories)
    
    # If no matches found for any keyword, use all categories as fallback
    if not all_matching_categories:
        all_matching_categories = SCAM_CATEGORIES
    
    # Remove duplicates and return random choice
    unique_categories = list(set(all_matching_categories))
    return random.choice(unique_categories)

# Generate image URLs as JSON string
def generate_image_urls():
    seed = random.randint(1, 10000)
    urls = [f"https://picsum.photos/seed/{seed}/640/480"]
    return json.dumps(urls)

# Generate video URLs as JSON string
def generate_video_urls():
    # Sometimes return empty, sometimes with mock video URLs
    if random.choice([True, False]):
        return json.dumps([])
    else:
        return json.dumps([f"https://example.com/video_{random.randint(1000, 9999)}.mp4"])

# Generate scam-related content
def generate_scam_info():
    scam_types = [
        "Investment Scam",
        "Romance Scam", 
        "Phishing Attempt",
        "Fake Product",
        "Cryptocurrency Fraud",
        "Tech Support Scam",
        "Not Detected",
        "Clean"
    ]
    return random.choice(scam_types)

def generate_scam_detail():
    details = [
        "Suspicious investment promises with unrealistic returns",
        "Fake romantic relationship to extract money",
        "Attempting to steal personal information through fake login pages",
        "Selling counterfeit or non-existent products",
        "Fraudulent cryptocurrency investment schemes",
        "Fake technical support requesting remote access",
        "No suspicious activity detected",
        "Content appears legitimate"
    ]
    return random.choice(details)

def generate_location():
    thai_locations = [
        "Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Krabi", 
        "Koh Samui", "Hua Hin", "Ayutthaya", "Chiang Rai", "Udon Thani"
    ]
    return random.choice(thai_locations)

def generate_advertiser():
    advertisers = [
        "Bangkok Investment Co.", "Thai Financial Group", "SE Asia Marketing",
        "Golden Opportunity Ltd.", "Future Wealth Thailand", "Digital Success Co.",
        "Thai Business Solutions", "Bangkok Trading Corp", "Siam Investment Ltd.",
        "Thailand Success Group"
    ]
    return random.choice(advertisers)

def filter_ads_by_keywords(ads, keywords):
    """Filter ads that contain any of the keywords in ad_text, page_name, or categories"""
    filtered = []
    keywords_lower = [kw.lower() for kw in keywords]
    
    for ad in ads:
        # Check if any keyword matches
        match_found = False
        for keyword in keywords_lower:
            if (keyword in ad["ad_text"].lower() or 
                keyword in ad["page_name"].lower() or
                any(keyword in cat.lower() for cat in ad["categories"])):
                match_found = True
                break
        
        if match_found:
            filtered.append(ad)
    
    return filtered

def parse_date_string(date_str):
    """Parse date string to timestamp"""
    if date_str.lower() == "today":
        return int(time.time())
    try:
        # Try to parse "June 18,2018" format
        return int(datetime.strptime(date_str, "%B %d,%Y").timestamp())
    except:
        # Default to a reasonable date if parsing fails
        return int(datetime(2018, 6, 18).timestamp())

# API endpoint: POST request with filtering
@app.post("/ads")
def search_ads(request: AdSearchRequest):
    # Generate base dataset
    now = int(time.time())
    start_timestamp = parse_date_string(request.start_date)
    end_timestamp = parse_date_string(request.end_date) if request.end_date != "today" else now
    
    # Generate more data than needed for filtering
    total_to_generate = min(request.limit * 2, 5000)  # Generate extra for filtering
    
    base_ads = []
    for i in range(total_to_generate):
        category = generate_keyword_based_category(request.keyword)
        # Use random keyword from the list for ad text
        selected_keyword = random.choice(request.keyword)
        
        ad = {
            "ad_archive_id": str(i),
            "page_name": fake.company(),
            "page_id": str(random.randint(1e14, 1e15)),
            "page_like_count": random.randint(100, 100000),
            "page_categories": [category],
            "cta_text": random.choice(["Send Message", "Learn More", "Shop Now", "Sign Up", "Call Now"]),
            "cta_type": random.choice(["MESSAGE_PAGE", "LEARN_MORE", "SHOP_NOW", "SIGN_UP", "CALL_NOW"]),
            "link_url": fake.url(),
            "impressions_text": f"{random.randint(1000, 100000):,} impressions",
            "start_date": random.randint(start_timestamp, end_timestamp),
            "end_date": random.randint(now, now + 604800),  # End date up to 7 days from now
            "ad_text": f"{selected_keyword} {fake.paragraph(nb_sentences=2)}",  # Include random keyword in ad text
            "image_urls": generate_image_urls(),
            "video_urls": generate_video_urls(),
            "categories": [category],
            "publisher_platforms": ["FACEBOOK", "INSTAGRAM"] if random.choice([True, False]) else ["FACEBOOK"],
            "collation_count": random.randint(1, 10),
            "entity_type": random.choice(["PERSON_PROFILE", "BUSINESS_PAGE", "ORGANIZATION"]),
            "total_active_time": random.randint(1000, 50000),
            "has_images": True,
            "has_videos": random.choice([True, False]),
            "has_clickable_link": True,
            "is_active": random.choice([True, False]),
            "contains_sensitive_content": random.choice([True, False]),
            "contains_digital_created_media": random.choice([True, False]),
            "is_aaa_eligible": random.choice([True, False]),
            "start_date_formatted": datetime.fromtimestamp(random.randint(start_timestamp, end_timestamp)).strftime("%Y-%m-%d"),
            "end_date_formatted": fake.date_between(start_date='today', end_date='+7d').strftime("%Y-%m-%d"),
            "follower_count": random.randint(100, 100000),
            "engagement_pct": random.randint(1, 30),
            "posts_count": random.randint(100, 1000),
            "caption_text": fake.paragraph(nb_sentences=2),
            "risk_threshold": random.randint(5, 100),
            "title_name": fake.job(),
            "tel": fake.phone_number(),
            "email": fake.email(),
            "scam_info": generate_scam_info(),
            "scam_url_content": fake.paragraph(nb_sentences=random.randint(1, 3)),
            "scam_detail": generate_scam_detail(),
            "location": generate_location(),
            "language": request.language,
            "advertiser": generate_advertiser(),
            "media_type": "image" if ad.get("has_images") else "text",
            "platform": random.choice(["facebook", "instagram", "all"]) if request.platform == "all" else request.platform
        }
        base_ads.append(ad)
    
    # Apply filters
    filtered_ads = base_ads
    
    # Filter by keywords (always applied since it's required)
    filtered_ads = filter_ads_by_keywords(filtered_ads, request.keyword)
    
    # Filter by location
    if request.location != "all":
        filtered_ads = [ad for ad in filtered_ads if ad["location"].lower() == request.location.lower()]
    
    # Filter by language
    if request.language != "all":
        filtered_ads = [ad for ad in filtered_ads if ad["language"].lower() == request.language.lower()]
    
    # Filter by advertiser
    if request.advertiser != "all":
        filtered_ads = [ad for ad in filtered_ads if request.advertiser.lower() in ad["advertiser"].lower()]
    
    # Filter by platform
    if request.platform != "all":
        filtered_ads = [ad for ad in filtered_ads if ad["platform"] == request.platform]
    
    # Filter by media type
    if request.media_type != "all":
        filtered_ads = [ad for ad in filtered_ads if ad["media_type"] == request.media_type]
    
    # Filter by status
    if request.status != "all":
        if request.status == "active":
            filtered_ads = [ad for ad in filtered_ads if ad["is_active"]]
        elif request.status == "inactive":
            filtered_ads = [ad for ad in filtered_ads if not ad["is_active"]]
    
    # Apply limit
    result = filtered_ads[:request.limit]
    
    return {
        "total_found": len(filtered_ads),
        "returned": len(result),
        "ads": result
    }
