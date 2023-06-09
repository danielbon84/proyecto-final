import Banner from "../../../img/banner.png";
import Bannermovil from "../../../img/bannermovil.png";
import React from "react";
import { Filtrados } from "../filtrados.jsx";

export const BannerPortada = () => {
  return (
    <>
      <div
        className="container-fluid d-block w-100 d-none d-md-block position-relative "
        style={{
          backgroundImage: `url(${Banner})`,
          backgroundSize: "cover",
          backgroundRepeat: "no-repeat",
          width: "100%",
          height: "500px",
        }}
      >
        <div className="col-lg-7 col-md-10 position-absolute p-5  top-50 start-0">
          <Filtrados />
        </div>
      </div>
      <div
        className="container-fluid position-relative d-md-none d-block w-100  "
        style={{
          backgroundImage: `url(${Bannermovil})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          width: "100%",
          height: "400px",
        }}
      >
        <div className="col-12 position-absolute py-4 bottom-0 start-0">
          <Filtrados />
        </div>
      </div>
    </>
  );
};
