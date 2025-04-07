# from flask import jsonify, render_template, request, redirect, url_for, session, flash
# from bson.objectid import ObjectId
# from app import app, mongo

# @app.route("/")
# def home():
    # try:
    #     items_collection = mongo.db.item

    #     lost_items = list(items_collection.find({"status": "lost"}).sort("dateLost", -1).limit(5))
    #     found_items = list(items_collection.find({"status": "found"}).
            # sort("dateFound", -1).limit(5))

    #     for item in lost_items + found_items:
    #         item["_id"] = str(item["_id"])

    #     recent_items = lost_items + found_items
    #     recent_items.sort(key=lambda x: x.get("dateLost", x.get("dateFound")), reverse=True)

    #     return render_template("index.html", recent_items=recent_items[:3])

    # except Exception as e:
    #     print(f"Error fetching recent items: {e}")
    #     return render_template("index.html", recent_items=[])
    # return

# if __name__ == '__main__':
    # app.run(debug=True)
