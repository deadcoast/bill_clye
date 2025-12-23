# python_styles.md - PYTHON DOCSTRING STYLES
[MRDR:doc:spec=doctags](/docs/doctags.md)

## 1. Sphinx (reStructuredText) Style

```python
def my_function(name, age):
    """
    This is a brief description of the function.

    :param name: The name of the user.
    :type name: str
    :param age: The age of the user.
    :type age: int
    :return: A greeting message.
    :rtype: str
    """
    return f"Hello {name}, you are {age} years old."

```

### 1.1 Sphinx Style: Rules

* **Summary Line:** Start with a concise, capitalized summary of the object's purpose ending in a period.
* **Structural Spacing:** Insert a blank line between the summary and the technical metadata/field lists.
* **Field Indentation:** Ensure all descriptions and sub-elements are consistently indented under their respective tags.
* **Clean Termination:** Place the closing triple-quotes on their own line to clearly demarcate the end of the block.

---

## 2. Google Style

```python
def my_function(name, age):
    """
    This is the module or function description.

    Args:
        name (str): The name of the user.
        age (int): The age of the user.

    Returns:
        str: A greeting message.
    """
    return f"Hello {name}, you are {age} years old."

```

### 2.1 Google Style: Rules

* **Summary Line:** Start with a concise, capitalized summary of the object's purpose ending in a period.
* **Structural Spacing:** Insert a blank line between the summary and the technical metadata/field lists.
* **Field Indentation:** Ensure all descriptions and sub-elements are consistently indented under their respective tags.
* **Clean Termination:** Place the closing triple-quotes on their own line to clearly demarcate the end of the block.

---

## 3. NumPy Style

```python
def my_function(name, age):
    """
    Brief description.

    Parameters
    ----------
    name : str
        The name of the user.
    age : int
        The age of the user.

    Returns
    -------
    str
        A greeting message.
    """

```

### 3.1 NumPy Style: Rules

* **Summary Line:** Start with a concise, capitalized summary of the object's purpose ending in a period.
* **Structural Spacing:** Insert a blank line between the summary and the technical metadata/field lists.
* **Field Indentation:** Ensure all descriptions and sub-elements are consistently indented under their respective tags.
* **Clean Termination:** Place the closing triple-quotes on their own line to clearly demarcate the end of the block.

---

## 4. Epytext Style

*Historically used by Epydoc; uses "@" symbols similar to Javadoc.*

```python
def my_function(name, age):
    """
    Brief description.

    @param name: The name of the user.
    @type name: str
    @return: A greeting message.
    """

```

### 4.1 Epytext Style: Rules

* **Summary Line:** Start with a concise, capitalized summary of the object's purpose ending in a period.
* **Structural Spacing:** Insert a blank line between the summary and the technical metadata/field lists.
* **Field Indentation:** Ensure all descriptions and sub-elements are consistently indented under their respective tags.
* **Clean Termination:** Place the closing triple-quotes on their own line to clearly demarcate the end of the block.

---

## 5. PEP 257 (Standard)

*The bare-minimum Python standard, typically used for simple functions or modules.*

```python
def my_function():
    """
    Perform a simple task and return None.

    This multi-line section expands on the summary above if
    more context is required for the developer.
    """
    pass

```

### 5.1 PEP 257 Style: Rules

* **Summary Line:** Start with a concise, capitalized summary of the object's purpose ending in a period.
* **Structural Spacing:** Insert a blank line between the summary and the technical metadata/field lists.
* **Field Indentation:** Ensure all descriptions and sub-elements are consistently indented under their respective tags.
* **Clean Termination:** Place the closing triple-quotes on their own line to clearly demarcate the end of the block.

---
