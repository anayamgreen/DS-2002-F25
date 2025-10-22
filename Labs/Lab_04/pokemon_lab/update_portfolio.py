import os
import sys
import json
import pandas as pd

def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    if not os.path.isdir(lookup_dir):
        return pd.DataFrame(columns=["card_id","card_name","card_number","set_id","set_name","card_market_value"])
    frames = []
    for fname in os.listdir(lookup_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(lookup_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception:
            continue
        if not isinstance(payload, dict) or "data" not in payload or not isinstance(payload["data"], list):
            continue

        df = pd.json_normalize(payload["data"])
        holo = df.get("tcgplayer.prices.holofoil.market")
        norm = df.get("tcgplayer.prices.normal.market")
        base = pd.Series([None] * len(df))
        df["card_market_value"] = ((holo if holo is not None else base).fillna(norm if norm is not None else 0.0)).fillna(0.0)

        df = df.rename(columns={
            "id": "card_id",
            "name": "card_name",
            "number": "card_number",
            "set.id": "set_id",
            "set.name": "set_name",
        })

        needed = ["card_id","card_name","card_number","set_id","set_name","card_market_value"]
        for c in needed:
            if c not in df.columns:
                df[c] = 0.0 if c == "card_market_value" else pd.NA

        frames.append(df[needed].copy())

    if not frames:
        return pd.DataFrame(columns=["card_id","card_name","card_number","set_id","set_name","card_market_value"])

    out = pd.concat(frames, ignore_index=True)
    out["card_market_value"] = pd.to_numeric(out["card_market_value"], errors="coerce").fillna(0.0)
    out = out.sort_values("card_market_value", ascending=False).drop_duplicates(subset=["card_id"], keep="first").reset_index(drop=True)
    return out

def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    if not os.path.isdir(inventory_dir):
        return pd.DataFrame(columns=["card_name","set_id","card_number","binder_name","page_number","slot_number","card_id"])

    frames = []
    for fname in os.listdir(inventory_dir):
        if fname.endswith(".csv"):
            fpath = os.path.join(inventory_dir, fname)
        # read csv, keep going on errors
            try:
                frames.append(pd.read_csv(fpath))
            except Exception:
                continue

    if not frames:
        return pd.DataFrame(columns=["card_name","set_id","card_number","binder_name","page_number","slot_number","card_id"])

    inv = pd.concat(frames, ignore_index=True)
    inv["set_id"] = inv["set_id"].astype(str)
    inv["card_number"] = inv["card_number"].astype(str)
    inv["card_id"] = inv["set_id"] + "-" + inv["card_number"]
    return inv

def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    final_cols = [
        "index","card_id","card_name","set_id","set_name",
        "card_number","binder_name","page_number","slot_number","card_market_value"
    ]

    if inventory_df.empty:
        print("Inventory is epmty", file=sys.stderr)
        pd.DataFrame(columns=final_cols).to_csv(output_file, index=False)
        return

    merged = pd.merge(inventory_df, lookup_df[["card_id","card_name","card_number","set_id","set_name","card_market_value"]], on="card_id",
        how="left"
    )

    merged["card_market_value"] = pd.to_numeric(merged["card_market_value"], errors="coerce").fillna(0.0)
    merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")

    merged["index"] = (
        merged["binder_name"].astype(str) + "-" +
        merged["page_number"].astype(str) + "-" +
        merged["slot_number"].astype(str)
    )

    merged[final_cols].to_csv(output_file, index=False)
    print(f"Wrote portfolio to {output_file}")

def main():
    update_portfolio("./card_inventory/", "./card_set_lookup/", "card_portfolio.csv")

def test():
    update_portfolio("./card_inventory_test/", "./card_set_lookup_test/", "test_card_portfolio.csv")

if __name__ == "__main__":
    print("Starting update_portfoli", file=sys.stderr)
    test()
