import React, { useState, useContext, useEffect } from "react";
import { AuthContext } from "../components/AuthContext";
import NFTCard from "../components/NFT Card";
import Loading from "../components/Loading";

function Favorite() {
  const { user } = useContext(AuthContext);
  const [ favoriteItems, setFavoriteItems ]= useState([]);
  console.log(favoriteItems)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/nfts/favorites/", {
      method: "GET",
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((response) => response.json())
      .then((data) => {
        const arr = data.favorites.map((nft) => ({
          id: nft.nft__id,
          name: nft.nft__name,
          image: `http://127.0.0.1:8000/media/${nft.nft__image}`,
          price: nft.nft__price,
          highest_bid: nft.nft__highest_bid,
          addTime: nft.nft__addTime,
        }));
        setFavoriteItems(arr);
      });
  },[]);

  if (!user) {
    return (
      <>
        <div id="stars"></div>
        <div id="stars2"></div>
        <div id="stars3"></div>
        <div className="container">
          <h3 className="view">
            Please sign in to view your favorites.&#128519;
          </h3>
        </div>
      </>
    );
  }

  if (favoriteItems && favoriteItems.length === 0) {
    return (
      <>
        <div id="stars"></div>
        <div id="stars2"></div>
        <div id="stars3"></div>
        <div className="container">
          <h3 className="view">You have no favorite items.&#128556;</h3>
        </div>
      </>
    );
  }

  return (
    <>
      <div id="stars"></div>
      <div id="stars2"></div>
      <div id="stars3"></div>
      <section className="about_head_section">
        <div className="container">
          <h1>Your Fav NFT</h1>
          <p>
            Every NFT purchase is a support for art and artists, as well as an
            opportunity to become the owner of a unique piece. Experience
            unforgettable emotions and create your own collection of digital
            assets that will grow and bring joy for many years to come.
          </p>
        </div>
      </section>
      <section className="nft_card_section">
        <div className="container">
          <div className="nft_cards_row j-flex">
            {favoriteItems?.map((item) => (
              <NFTCard key={item.id} nft={item} />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

export default Favorite;