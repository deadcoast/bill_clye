"""UDL validation utilities.

This module provides validation functions for UDL definitions,
ensuring delimiters and operators conform to the specification.
"""

from pydantic import ValidationError as PydanticValidationError

from mrdr.database.udl.schema import UDLDefinition, UDLOperator


class UDLValidationError(Exception):
    """UDL validation failed.

    Attributes:
        field: The field that failed validation.
        value: The invalid value.
        expected: Description of expected value.
    """

    def __init__(self, field: str, value: str, expected: str) -> None:
        self.field = field
        self.value = value
        self.expected = expected
        super().__init__(f"Invalid {field}: '{value}' (expected {expected})")


class UDLValidator:
    """Validator for UDL definitions and operators."""

    @staticmethod
    def validate_delimiter(value: str, field_name: str = "delimiter") -> str:
        """Validate that a delimiter is exactly 1 character.

        Args:
            value: The delimiter value to validate.
            field_name: Name of the field for error messages.

        Returns:
            The validated delimiter.

        Raises:
            UDLValidationError: If the delimiter is not exactly 1 character.
        """
        if len(value) != 1:
            raise UDLValidationError(
                field=field_name,
                value=value,
                expected="exactly 1 character",
            )
        return value

    @staticmethod
    def validate_operator_delimiter(
        value: str, field_name: str = "operator"
    ) -> str:
        """Validate that an operator delimiter is exactly 2 characters.

        Args:
            value: The operator delimiter value to validate.
            field_name: Name of the field for error messages.

        Returns:
            The validated operator delimiter.

        Raises:
            UDLValidationError: If the operator is not exactly 2 characters.
        """
        if len(value) != 2:
            raise UDLValidationError(
                field=field_name,
                value=value,
                expected="exactly 2 characters",
            )
        return value

    @staticmethod
    def validate_operator(operator: UDLOperator) -> UDLOperator:
        """Validate a complete UDL operator.

        Args:
            operator: The operator to validate.

        Returns:
            The validated operator.

        Raises:
            UDLValidationError: If the operator is invalid.
        """
        UDLValidator.validate_operator_delimiter(operator.open, "operator.open")
        UDLValidator.validate_operator_delimiter(operator.close, "operator.close")
        return operator

    @staticmethod
    def validate_definition(definition: UDLDefinition) -> UDLDefinition:
        """Validate a complete UDL definition.

        Args:
            definition: The definition to validate.

        Returns:
            The validated definition.

        Raises:
            UDLValidationError: If the definition is invalid.
        """
        UDLValidator.validate_delimiter(
            definition.delimiter_open, "delimiter_open"
        )
        UDLValidator.validate_delimiter(
            definition.delimiter_close, "delimiter_close"
        )
        for op in definition.operators:
            UDLValidator.validate_operator(op)
        return definition

    @staticmethod
    def validate_definition_dict(data: dict) -> UDLDefinition:
        """Validate and create a UDL definition from a dictionary.

        Args:
            data: Dictionary containing UDL definition fields.

        Returns:
            A validated UDLDefinition instance.

        Raises:
            UDLValidationError: If validation fails.
        """
        try:
            definition = UDLDefinition(**data)
            return UDLValidator.validate_definition(definition)
        except PydanticValidationError as e:
            # Extract first error for cleaner message
            first_error = e.errors()[0]
            field = ".".join(str(loc) for loc in first_error["loc"])
            raise UDLValidationError(
                field=field,
                value=str(first_error.get("input", "")),
                expected=first_error["msg"],
            ) from e
