=======
History
=======

1.0.0 (2017-6-11)
-----------------

* Drop support for python 2.6, add support for python 3.5, python 3.6 and pypy
* Fix issue `#35 <https://github.com/Trax-air/swagger-parser/issues/35>`_
* `Add file parser tests and fixes for #40, #41, #42, #43, #44, #45 <https://github.com/Trax-air/swagger-parser/pull/39>`_, thanks to @mtherieau
* `Use isinstance for simple type checking <https://github.com/Trax-air/swagger-parser/pull/36>`_, thanks to @pankaj28843
* `Fixes for #31, #32, #33 <https://github.com/Trax-air/swagger-parser/pull/34>`_, thanks to @crudo10 and @beanqueen for the review
* `Bug fix when dictionary only contains 1 element <https://github.com/Trax-air/swagger-parser/pull/30>`_, thanks to @TenOs
* `Add tests for "official" petstore json and yaml <https://github.com/Trax-air/swagger-parser/pull/29>`_, thanks to @beanqueen


0.1.11 (2016-9-25)
------------------

* Support additionalProperties.

0.1.10 (2016-8-25)
------------------

* Don't choke if there are no definitions
* Generate operations without operationId
* Generate example from properties

0.1.9 (2016-7-28)
------------------

* Support array definitions.

0.1.8 (2016-5-11)
------------------

* Support type field to be an array.
* Use base path to validate request.

0.1.7 (2016-4-1)
------------------

* Support UTF-8 in swagger.yaml.

0.1.6 (2016-3-16)
------------------

* Add support for path-level parameters.

0.1.5 (2016-2-17)
------------------

* Add support for parameters references in path specs.

0.1.4 (2016-2-10)
------------------

* Handle string as status_code.

0.1.3 (2016-2-3)
------------------

* Fix a bug in get_response_example with schema only containing a type field.

0.1.2 (2016-2-3)
------------------

* Support schema with only a type field.

0.1.1 (2016-1-31)
------------------

* Change license to MIT.

0.1 (2016-1-28)
------------------

* First release on PyPI.
