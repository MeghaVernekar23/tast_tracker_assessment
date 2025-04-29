import React from "react";

export const AlertMessage = ({ show, type = "success", message }) => {
  if (!show) return null;

  return (
    <div className={`alert alert-${type} mt-3`} role="alert">
      {message}
    </div>
  );
};
