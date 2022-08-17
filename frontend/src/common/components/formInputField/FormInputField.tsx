import React, {useState} from "react";

import {dotted} from "../../utils";
import FormDateInputField from "./FormDateInputField";
import FormDropdownInputField from "./FormDropdownInputField";
import FormMoneyInputField from "./FormMoneyInputField";
import FormPostalCodeInputField from "./FormPostalCodeInputField";
import FormTextInputField from "./FormTextInputField";

export interface CommonFormInputFieldProps {
    id: string;
    key: string;
    label: string;
    value: string;
    required?: boolean;
    setFieldValue: (value) => void;
}

type FormInputFieldProps = {
    label: string;
    fieldPath: string;
    validator?: (value) => boolean;
    required?: boolean;
    formData: object;
    setFormData: (draft) => void;
} & (
    | {
          inputType?: "text" | "textArea" | "postalCode" | "money" | "date";
      }
    | {
          inputType: "select" | "combobox";
          options: {label: string}[];
      }
    | {
          inputType: "relatedModel";
          options?: never;
          queryFunction;
          relatedModelSearchField: string;
          getRelatedModelLabel: (unknown) => string;
      }
);

export default function FormInputField({
    inputType = "text",
    label,
    fieldPath,
    required,
    validator,
    formData,
    setFormData,
    ...rest
}: FormInputFieldProps): JSX.Element {
    const [isInvalid, setIsInvalid] = useState(false);

    const setFieldValue = (value) => {
        if (validator !== undefined) setIsInvalid(!validator(value));
        else if (required) setIsInvalid(!value);

        setFormData((draft) => {
            dotted(draft, fieldPath, value);
        });
    };

    const commonProps = {
        id: `input-${fieldPath}`,
        key: `input-${fieldPath}`,
        label: label,
        value: dotted(formData, fieldPath) || "",
        required: required,
        invalid: isInvalid,
        setFieldValue: setFieldValue,
    };

    if (inputType === "text" || inputType === "textArea") {
        return (
            <FormTextInputField
                {...commonProps}
                size={inputType === "text" ? "small" : "large"}
                {...rest}
            />
        );
    } else if (inputType === "postalCode") {
        return (
            <FormPostalCodeInputField
                {...commonProps}
                setIsInvalid={setIsInvalid}
                {...rest}
            />
        );
    } else if (inputType === "money") {
        return (
            <FormMoneyInputField
                {...commonProps}
                {...rest}
            />
        );
    } else if (inputType === "combobox" || inputType === "select") {
        if (!("options" in rest) || rest.options === undefined || !rest.options.length)
            throw new Error("`options` argument is required when `inputType` is `select` or `combobox`.");

        return (
            <FormDropdownInputField
                {...commonProps}
                searchable={inputType === "combobox"}
                {...rest}
            />
        );
    } else if (inputType === "date") {
        return (
            <FormDateInputField
                {...commonProps}
                setIsInvalid={setIsInvalid}
                {...rest}
            />
        );
    }
    throw new Error("Invalid `inputType` given.");
}
