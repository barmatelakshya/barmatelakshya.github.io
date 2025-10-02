#!/bin/bash
echo "🧹 TrustEye Cleanup - Removing Duplicate Files"
echo "=============================================="

# List of duplicate files to remove
duplicates=(
    "trusteye_dashboard.html"
    "trusteye_demo.html"
    "trusteye.html"
    "trusteye_styled.py"
    "trusteye_simple.py"
    "trusteye_online.py"
    "trusteye_working.py"
)

echo "📁 Files to be removed:"
for file in "${duplicates[@]}"; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || echo "0")
        echo "  ❌ $file (${size} bytes)"
    fi
done

echo ""
read -p "🗑️ Remove these duplicate files? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning up..."
    
    for file in "${duplicates[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "✅ Removed: $file"
        fi
    done
    
    echo ""
    echo "🎉 Cleanup completed!"
    echo "📁 Remaining core files:"
    echo "  ✅ trusteye_fixed.html (Main app)"
    echo "  ✅ trusteye_single.py (Server)"
    echo "  ✅ start_trusteye.sh (Startup)"
    
else
    echo "❌ Cleanup cancelled"
fi

echo ""
echo "🚀 To run TrustEye:"
echo "   ./start_trusteye.sh"
