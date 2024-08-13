// This file is part of InvenioRDM
// Copyright (C) 2024 TU Wien.
//
// Invenio-Curations is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { i18next } from "@translations/invenio_requests/i18next";
import { Button } from "semantic-ui-react";

const RequestBaseButton = (props) => {
  const { onClick, loading, ariaAttributes, size, content, className, icon, color } =
    props;

  return (
    <Button
      icon={icon}
      labelPosition="left"
      content={content}
      onClick={onClick}
      negative={color === "negative"}
      positive={color === "positive"}
      loading={loading}
      disabled={loading}
      size={size}
      className={className}
      {...ariaAttributes}
    />
  );
};

export const RequestCritiqueButton = (props) => {
  return RequestBaseButton({
    icon: "exclamation circle",
    color: "negative",
    content: i18next.t("Request changes"),
    ...props,
  });
};

export const RequestResubmitButton = (props) => {
  return RequestBaseButton({
    icon: "paper hand outline",
    color: "neutral",
    content: i18next.t("Resubmit for review"),
    ...props,
  });
};

export const RequestReviewButton = (props) => {
  return RequestBaseButton({
    icon: "eye",
    color: "neutral",
    content: i18next.t("Start review"),
    ...props,
  });
};