# CHANGELOG



## v2.0.1 (2024-03-03)

### Documentation

* docs: add ruff badge ([`d4281b1`](https://github.com/Rizhiy/replete/commit/d4281b181bf903eedd101ae52940283c524dc239))

### Fix

* fix: try to trigger release again ([`711bdd8`](https://github.com/Rizhiy/replete/commit/711bdd80e4a082e8a5a7e1f8d3800c13eb5d7db5))


## v2.0.0 (2024-03-03)

### Breaking

* refactor: fix ruff errors

BREAKING CHANGE: ([`8d1a119`](https://github.com/Rizhiy/replete/commit/8d1a119cb9a15c87ecbc25775d71c5d7467c19b2))

### Chore

* chore(utils): remove redundant bisect functions, no longer requried ([`e4bd7f3`](https://github.com/Rizhiy/replete/commit/e4bd7f3b7742282f5f548ec59030871a1ef53b00))

* chore: begin process to publish to pypi ([`7d8172f`](https://github.com/Rizhiy/replete/commit/7d8172ffd4e9bbad9a9097c76d51f377e6d5f2a0))

### Documentation

* docs: update README.md ([`ead579a`](https://github.com/Rizhiy/replete/commit/ead579aca421715054252983cd01cbc74cabde17))

### Fix

* fix: commit to trigger publish ([`5b1d25a`](https://github.com/Rizhiy/replete/commit/5b1d25adae24b3db1757c6d07e3d15771c9f0cf9))

* fix: drop support for python 3.9 ([`a659887`](https://github.com/Rizhiy/replete/commit/a6598875e6bd79c9f87eb3797f8648ec67b25341))

### Test

* test: rename imports in tests ([`a34c835`](https://github.com/Rizhiy/replete/commit/a34c8357ef9cd39f05676c33edb7c91ff72a7370))


## v1.15.1 (2023-10-13)

### Unknown

* 1.15.1

Feature
* **cli.py:** Improve parse_bool (5e2f1f0)
* **logging.py:** Improve logging of uncaught exceptions and whitelist (7b2bd8e) ([`2c90f37`](https://github.com/Rizhiy/replete/commit/2c90f3744f5d45128271eb94435cc9717ef42082))

* imp(cli.py): Improve parse_bool ([`5e2f1f0`](https://github.com/Rizhiy/replete/commit/5e2f1f0b779f0ae81f9b7a2eee9d0502add3e38a))

* imp(logging.py): Improve logging of uncaught exceptions and whitelist ([`7b2bd8e`](https://github.com/Rizhiy/replete/commit/7b2bd8eb30bdfe77a0dff8d7e2cdfde3be470488))


## v1.15.0 (2023-06-26)

### Feature

* feat(funcutils.py): Add yield_or_skip ([`05552cd`](https://github.com/Rizhiy/replete/commit/05552cd3de107a1d669f00fc13e35e6753588300))

### Fix

* fix(logging.py): Refactor code and rework adding of handler logic ([`3225fac`](https://github.com/Rizhiy/replete/commit/3225fac1dca07938601c58d33e42b7a76058890d))

### Test

* test(test_utils.py): Relax the requirements on futures_processing time to allow passing on slower computers ([`624eb43`](https://github.com/Rizhiy/replete/commit/624eb4342cb2e2e5f9eb80dcbd2c3b6f71fa23cf))

* test(test_utils.py): Add flaky to futures_processing tests ([`365df1a`](https://github.com/Rizhiy/replete/commit/365df1a1893170cac499b30b7ff31740088b9df5))

### Unknown

* 1.15.0

Feature
* **logging.py:** Add whitelist to setup_logging (c79ea9b)
* **funcutils.py:** Add yield_or_skip (05552cd)
* **timing.py:** Change default Timer behaviour to include sleep (0f30688)

Fix
* **logging.py:** Refactor code and rework adding of handler logic (3225fac) ([`3a10bd1`](https://github.com/Rizhiy/replete/commit/3a10bd1cc529fd7d62973150be1524ee146ccfe3))

* imp(logging.py): Add whitelist to setup_logging ([`c79ea9b`](https://github.com/Rizhiy/replete/commit/c79ea9bc92b0fd46809d69e29f76a98e9cb3344c))

* imp(timing.py): Change default Timer behaviour to include sleep

BREAKING_CHANGE: Timer now includes sleep by default, use process_only
to disable. include_sleep is removed. ([`0f30688`](https://github.com/Rizhiy/replete/commit/0f306887a4bdffb90678a8c1d91f3a3025861929))


## v1.14.0 (2023-05-28)

### Feature

* feat(utils.py): Add weak_lru_cache ([`090f30b`](https://github.com/Rizhiy/replete/commit/090f30babb4b5d96202630c17b6b054c3620291f))

### Unknown

* 1.14.0

Feature
* **utils.py:** Add weak_lru_cache (090f30b) ([`f830fff`](https://github.com/Rizhiy/replete/commit/f830fff25bdc3f153a3d7530f8a83ea2c64f8729))


## v1.13.1 (2023-02-21)

### Unknown

* 1.13.1

Feature
* **__init__.py:** Add setup_logging and assert_with_logging to top level (f6d536c) ([`6a89133`](https://github.com/Rizhiy/replete/commit/6a8913327ce1ff473fedabf9206b97b2f617dba9))

* imp(__init__.py): Add setup_logging and assert_with_logging to top level ([`f6d536c`](https://github.com/Rizhiy/replete/commit/f6d536cdd51f343c0e77c0556c6cf1748602e7c0))


## v1.13.0 (2023-02-20)

### Documentation

* docs(README.md): Update nt-tools to nt-dev ([`63aaee3`](https://github.com/Rizhiy/replete/commit/63aaee39a2f352cf5edc0e25978f4b60c339d66e))

### Feature

* feat(logging.py): Add setup_logging from ntf ([`b39ab9e`](https://github.com/Rizhiy/replete/commit/b39ab9eb58009100d1422bdfae4e2653354d0c67))

### Test

* test(.gitlab-ci.yml): Remove strict mypy stage ([`6687373`](https://github.com/Rizhiy/replete/commit/6687373d4190d2acb16116b61212cb24516c0d74))

### Unknown

* 1.13.0

Feature
* **logging.py:** Add setup_logging from ntf (b39ab9e)

Documentation
* **README.md:** Update nt-tools to nt-dev (63aaee3) ([`07d37c5`](https://github.com/Rizhiy/replete/commit/07d37c54b089cee9cf83baf82f0c65c5a1d636e6))


## v1.12.4 (2023-02-17)

### Unknown

* 1.12.4

Feature
* **utils.py:** Add option to still raise exception in futures_processing (43502d4)
* **utils.py:** Improve exception handling in futures_processing (61fa952) ([`5096000`](https://github.com/Rizhiy/replete/commit/509600083a174fb07e979d5e428060b3e42c3d8e))

* imp(utils.py): Add option to still raise exception in futures_processing ([`43502d4`](https://github.com/Rizhiy/replete/commit/43502d4714b67ea8d03e4a4d67e0a8fad2b9b70f))

* imp(utils.py): Improve exception handling in futures_processing ([`61fa952`](https://github.com/Rizhiy/replete/commit/61fa952c051f1f3192237096176e854dece2cbf2))


## v1.12.3 (2023-02-16)

### Unknown

* 1.12.3

Feature
* **timing.py:** Add default weight for check_rate (4bae323) ([`7085088`](https://github.com/Rizhiy/replete/commit/7085088008565a539b7f00ff6d062b9feb537bd7))

* imp(timing.py): Add default weight for check_rate ([`4bae323`](https://github.com/Rizhiy/replete/commit/4bae3236eabc40b81a334bac9bf0a45ad74e5600))


## v1.12.2 (2023-02-16)

### Fix

* fix(timing.py): Add check for sub-zero sleep time ([`97e75d6`](https://github.com/Rizhiy/replete/commit/97e75d6e42f4f1283eb209a52a16af8c39fe8f1d))

### Test

* test(test_timing.py): Relax timing strictness ([`e23f0ef`](https://github.com/Rizhiy/replete/commit/e23f0efc962050570394e81ca821e6728236bef1))

* test(test_timing.py): Update argument name ([`b2d7b6e`](https://github.com/Rizhiy/replete/commit/b2d7b6e99a175c77db37b9e321b31d4bb3b2c2b9))

### Unknown

* 1.12.2

Fix
* **timing.py:** Add check for sub-zero sleep time (97e75d6) ([`b23c909`](https://github.com/Rizhiy/replete/commit/b23c90937e93fa5b7f6c21dd86d4a394a24fd9ec))


## v1.12.1 (2023-02-15)

### Unknown

* 1.12.1

Feature
* **utils.py:** Remove tqdm from futures_processing (7411f36) ([`3d84926`](https://github.com/Rizhiy/replete/commit/3d84926f5c0ca893064100ec3349624a5b8393b9))

* imp(utils.py): Remove tqdm from futures_processing ([`7411f36`](https://github.com/Rizhiy/replete/commit/7411f36dd24c1e55c885b3f74b37c7a23c273151))


## v1.12.0 (2023-02-15)

### Feature

* feat(utils.py): Add function for easy concurrent processing using futures ([`0b543dc`](https://github.com/Rizhiy/replete/commit/0b543dc47f1a7ea4a300988ff80f6f3524cddc59))

* feat(timing.py): Add RateLimiter class ([`ca3653d`](https://github.com/Rizhiy/replete/commit/ca3653dbdca21022b7519fca203d2f996745bfc9))

### Test

* test(.gitlab-ci.yml): Remove check-yamlfix, since it is now in template ([`256211b`](https://github.com/Rizhiy/replete/commit/256211b76edcc4e6f5e5005f07ee42c5a9fc34f3))

### Unknown

* 1.12.0

Feature
* **utils.py:** Add function for easy concurrent processing using futures (0b543dc)
* **timing.py:** Add RateLimiter class (ca3653d) ([`ccb4b65`](https://github.com/Rizhiy/replete/commit/ccb4b6532db2c95f4e1feac83c836bac4030c544))


## v1.11.1 (2023-01-15)

### Fix

* fix(enum.py): Fix hashing for ComparableEnum ([`bcd8b24`](https://github.com/Rizhiy/replete/commit/bcd8b24d9d32460b6303a7d8a92e58090916347c))

### Unknown

* 1.11.1

Fix
* **enum.py:** Fix hashing for ComparableEnum (bcd8b24) ([`0ccb894`](https://github.com/Rizhiy/replete/commit/0ccb894e833cfee52cf0df7dc8b7306cdd507eee))


## v1.11.0 (2023-01-14)

### Feature

* feat(enum.py): Add ComparableEnum ([`3992775`](https://github.com/Rizhiy/replete/commit/39927756ee7d23990bf1c46785cd7e2bca40e476))

### Test

* test: Update imports in test to highest possible level ([`97fe7db`](https://github.com/Rizhiy/replete/commit/97fe7db70d8eed6112f10c75c381e7a5e657eac7))

### Unknown

* 1.11.0

Feature
* **enum.py:** Add ComparableEnum (3992775) ([`0074b1d`](https://github.com/Rizhiy/replete/commit/0074b1d27292f9b21c889f93bc8622a0ff562ffc))


## v1.10.0 (2023-01-13)

### Feature

* feat(datetime.py): Move datetime ranges into separate file and add round_dt ([`3be1a54`](https://github.com/Rizhiy/replete/commit/3be1a54336c0d5beed852156dd7870874091e73e))

### Test

* test(pyproject.toml): Change optional dependency name from &#39;tests&#39; to &#39;test&#39; ([`9164b56`](https://github.com/Rizhiy/replete/commit/9164b566a1841b835e12be0b20fea95e8dff97bd))

### Unknown

* 1.10.0

Feature
* **datetime.py:** Move datetime ranges into separate file and add round_dt (3be1a54) ([`b80674b`](https://github.com/Rizhiy/replete/commit/b80674b16e8a82ee1870ae04439af5be56405763))


## v1.9.1 (2023-01-07)

### Style

* style(test_register.py): Fix fixture declaration ([`dd46254`](https://github.com/Rizhiy/replete/commit/dd46254e2fe20a5c46f500e2df10a67120be0d17))

### Test

* test(test_register.py): Add test for double registering ([`8e045af`](https://github.com/Rizhiy/replete/commit/8e045afb63d31c7123f7101a785c566735ea8b65))

* test(test_register.py): Add tests for Register ([`ffb92cf`](https://github.com/Rizhiy/replete/commit/ffb92cfc98090232af4b7d0bae1c26aa602aed41))

### Unknown

* 1.9.1

Feature
* **register.py:** Add Register.get_all_subclasses() (6301df8) ([`425a0dd`](https://github.com/Rizhiy/replete/commit/425a0dd38ec2aa09140a729d92fe68a1d26e8faf))

* imp(register.py): Add Register.get_all_subclasses() ([`6301df8`](https://github.com/Rizhiy/replete/commit/6301df815fc5b0156721518134df01d04aa35ac2))


## v1.9.0 (2022-12-05)

### Documentation

* docs(README.md): Fix badges ([`7653851`](https://github.com/Rizhiy/replete/commit/7653851edfe9d579dffcc774ca0c5107a82aee27))

### Feature

* feat(register.py): Add subclass tracking class ([`fc3b385`](https://github.com/Rizhiy/replete/commit/fc3b3853f90321b56076f49a65f9bfaf369dccb6))

### Unknown

* 1.9.0

Feature
* **register.py:** Add subclass tracking class (fc3b385)

Documentation
* **README.md:** Fix badges (7653851) ([`1ac4c4f`](https://github.com/Rizhiy/replete/commit/1ac4c4f1276293de34ffc493e974f09feb50e3e3))


## v1.8.2 (2022-12-03)

### Fix

* fix: Fix for version bump ([`a86e909`](https://github.com/Rizhiy/replete/commit/a86e909f91b2ab8e2969af541abe6203e6297e18))

### Test

* test(.gitlab-ci.yml): Fix include ([`611fc9b`](https://github.com/Rizhiy/replete/commit/611fc9bac9a873cbff742424d0eda562367ea69b))

### Unknown

* 1.8.2

Fix
* Fix for version bump (a86e909) ([`add036b`](https://github.com/Rizhiy/replete/commit/add036b86f697e8c17853c139d05a5c9c64bea76))


## v1.8.1 (2022-12-03)

### Fix

* fix(.gitlab-ci.yml): Update reference ([`c4ea0ba`](https://github.com/Rizhiy/replete/commit/c4ea0ba70ca1c8508bf3037dfef9a779f0161a58))

### Test

* test: Fix tests ([`52bb6af`](https://github.com/Rizhiy/replete/commit/52bb6aff9713da5d4d15c7ac3a7e18f2763f96f0))

### Unknown

* 1.8.1

Fix
* **.gitlab-ci.yml:** Update reference (c4ea0ba) ([`c701e4e`](https://github.com/Rizhiy/replete/commit/c701e4ee2c2910cce4e63b3ec741b90750616b81))


## v1.8.0 (2022-07-10)

### Feature

* feat(logging.py): Add context manger to temporarily change logging level ([`de087f4`](https://github.com/Rizhiy/replete/commit/de087f4357622587b8a8eb43a2e6dd3a9436ac9f))

### Fix

* fix(logging.py): Remove skip_handlers from change_logging_level, since it didn&#39;t work as expected ([`d248322`](https://github.com/Rizhiy/replete/commit/d248322b09df9f2ed26fb353bb65688ba5d5ef3c))

### Unknown

* 1.8.0

Feature
* **logging.py:** Add context manger to temporarily change logging level (de087f4)

Fix
* **logging.py:** Remove skip_handlers from change_logging_level, since it didn&#39;t work as expected (d248322) ([`92065ee`](https://github.com/Rizhiy/replete/commit/92065ee877aa87a74de553b773cf617e2b961db7))


## v1.7.0 (2022-07-07)

### Feature

* feat(timer.py): Add Timer ([`24df5ef`](https://github.com/Rizhiy/replete/commit/24df5ef520b563075b46ef09ca2910184e4c61a7))

### Unknown

* 1.7.0

Feature
* **timer.py:** Add Timer (24df5ef) ([`d4d9cd0`](https://github.com/Rizhiy/replete/commit/d4d9cd0ef043d92bc5a133294fd12516e11e1536))


## v1.6.0 (2022-06-28)

### Feature

* feat(logging.py): Add contextmanager which prints stacktrace for warnings ([`9819ca5`](https://github.com/Rizhiy/replete/commit/9819ca52713f3d6e173be56918980c26838b1c8d))

### Unknown

* 1.6.0

Feature
* **logging.py:** Add contextmanager which prints stacktrace for warnings (9819ca5) ([`476d0fb`](https://github.com/Rizhiy/replete/commit/476d0fb57618bac01a1f628c97e9d448ae5d92e5))


## v1.5.0 (2022-05-13)

### Feature

* feat(utils): `split_list` ([`e34a800`](https://github.com/Rizhiy/replete/commit/e34a800ca124b9548794ca2e7e183d200cbfb4bb))

### Refactor

* refactor: typing refactorings ([`820dcf3`](https://github.com/Rizhiy/replete/commit/820dcf34139905a85126681d079738c41f437106))

* refactor: flake8-guided style fixes ([`7189c50`](https://github.com/Rizhiy/replete/commit/7189c501607376765803daecd73b2b723d33e8b1))

### Unknown

* 1.5.0

Feature
* **utils:** `split_list` (e34a800) ([`0e69ad0`](https://github.com/Rizhiy/replete/commit/0e69ad02f6dd276109d4cc5b837267b96883176c))

* Merge branch &#39;feat_split_list&#39; into &#39;master&#39;

feat(utils): `split_list`

See merge request utilities/nt-utils!36 ([`3590035`](https://github.com/Rizhiy/replete/commit/3590035f6d42749aec1e204065ab3521d6c7dda8))

* Merge branch &#39;refactor_style_fixes&#39; into &#39;master&#39;

refactor: typing refactorings

See merge request utilities/nt-utils!35 ([`4385e5d`](https://github.com/Rizhiy/replete/commit/4385e5d8090b43e7df8508fa22d47b0168762423))

* Merge branch &#39;refactor_style_fixes&#39; into &#39;master&#39;

refactor: flake8-guided style fixes

See merge request utilities/nt-utils!34 ([`db74002`](https://github.com/Rizhiy/replete/commit/db7400201893dc917ca5f0ff006d33d6f5230d72))


## v1.4.0 (2022-03-28)

### Feature

* feat(utils): `window` ([`4bbdf3d`](https://github.com/Rizhiy/replete/commit/4bbdf3dc043ace3d5031eaea21f91f409c77cb89))

### Unknown

* 1.4.0

Feature
* **utils:** `window` (4bbdf3d) ([`637bf7e`](https://github.com/Rizhiy/replete/commit/637bf7e29a7db11c647c24cd6b1153c99a08f12f))

* Merge branch &#39;feat_window&#39; into &#39;master&#39;

feat(utils): `window`

See merge request utilities/nt-utils!33 ([`bfa8122`](https://github.com/Rizhiy/replete/commit/bfa812236a36ead7e7868032b731c2c32ae3e776))


## v1.3.0 (2022-03-16)

### Feature

* feat(utils): `iterchunks` ([`5dbd1b1`](https://github.com/Rizhiy/replete/commit/5dbd1b1b24cdb16c12e4aa548e0cfc8dc2522874))

### Unknown

* 1.3.0

Feature
* **utils:** `iterchunks` (5dbd1b1) ([`74c700e`](https://github.com/Rizhiy/replete/commit/74c700e6e2acdedb0b9cb33b6cd54d6a8a9bc8fc))

* Merge branch &#39;feat_iterchunks&#39; into &#39;master&#39;

feat(utils): `iterchunks`

See merge request utilities/nt-utils!32 ([`333e64e`](https://github.com/Rizhiy/replete/commit/333e64e082a842681bf2c8d4db91eb5789b50e37))


## v1.2.1 (2022-03-05)

### Unknown

* 1.2.1 ([`b2147d6`](https://github.com/Rizhiy/replete/commit/b2147d683274bf5ed18c72b9142592f5e84b47f5))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

revert(funcutils): remove `cached_property` in favor of `functools.cached_property`

See merge request utilities/nt-utils!31 ([`6154e42`](https://github.com/Rizhiy/replete/commit/6154e42ccfa5dfdcdba1a2dc4841c20df97ffa96))

* revert(funcutils): remove `cached_property` in favor of `functools.cached_property` ([`d333108`](https://github.com/Rizhiy/replete/commit/d333108faae6729ced120281698f48df11429bfa))


## v1.2.0 (2022-03-05)

### Feature

* feat(funcutils): cached_property ([`8df6d57`](https://github.com/Rizhiy/replete/commit/8df6d579cc532a4cbcc8b6889602b1fdf69826f2))

### Unknown

* 1.2.0

Feature
* **funcutils:** Cached_property (8df6d57) ([`ceb11ca`](https://github.com/Rizhiy/replete/commit/ceb11cac7d8607be46e03ceca7591b054418c736))

* Merge branch &#39;feat_cached_property&#39; into &#39;master&#39;

feat(funcutils): cached_property

See merge request utilities/nt-utils!30 ([`9da00e3`](https://github.com/Rizhiy/replete/commit/9da00e3ac7858f62a31f19a99b2a455d14383d7e))


## v1.1.0 (2022-03-02)

### Feature

* feat(consistent_hash): `picklehash` ([`4716e06`](https://github.com/Rizhiy/replete/commit/4716e0640e7ed71265fbb906fc1b30757d6b2bbd))

### Unknown

* 1.1.0

Feature
* **consistent_hash:** `picklehash` (4716e06) ([`297c037`](https://github.com/Rizhiy/replete/commit/297c0377840a1c31d9a6df7daedda0cf59588860))

* Merge branch &#39;feat_picklehash&#39; into &#39;master&#39;

feat(consistent_hash): `picklehash`

See merge request utilities/nt-utils!29 ([`0db69e3`](https://github.com/Rizhiy/replete/commit/0db69e3e240450162832f5b9ffc7ce5db3519ce2))


## v1.0.0 (2022-02-25)

### Breaking

* perf(consistent_hash): various performance improvements

BREAKING CHANGE: `consistent_hash` now returns an int64-compatible value to avoid overflows in `hash()`; `consistent_hash_raw` is replaced with mutating `consistent_hash_raw_update` ([`d7d93fd`](https://github.com/Rizhiy/replete/commit/d7d93fd35d9794baa7a45eb3364fbf2b4ee6e381))

### Unknown

* 1.0.0

Breaking
* `consistent_hash` now returns an int64-compatible value to avoid overflows in `hash()`; `consistent_hash_raw` is replaced with mutating `consistent_hash_raw_update`  (d7d93fd)

Performance
* **consistent_hash:** Various performance improvements (d7d93fd) ([`8ee6c71`](https://github.com/Rizhiy/replete/commit/8ee6c7165852ace6fd2ea9d4acaa8aa7ad4c2d6b))

* Merge branch &#39;perf_consistent_hash&#39; into &#39;master&#39;

perf(consistent_hash): various performance improvements

See merge request utilities/nt-utils!28 ([`90e4e02`](https://github.com/Rizhiy/replete/commit/90e4e02abb5762c2f533eb021cad8aab2ba37c80))


## v0.12.2 (2022-02-24)

### Chore

* chore: `doctest-modules` through pytest config ([`d3eca1f`](https://github.com/Rizhiy/replete/commit/d3eca1fa5efeac76e2d1602ab6dffc554e46f0a4))

* chore: yamlfix, typing containers fix ([`f2b5b10`](https://github.com/Rizhiy/replete/commit/f2b5b10d49efaa664f9094ee1a9c3cfd57cbaa1a))

### Documentation

* docs(README.md): Fix badges ([`05664b2`](https://github.com/Rizhiy/replete/commit/05664b2848e23acb6f44603cdbb6de52525a8c6f))

### Fix

* fix(consistent_hash): support classes in `consistent_hash` (ignore non-bound `_consistent_hash` methods) ([`6817fb0`](https://github.com/Rizhiy/replete/commit/6817fb0074d9619d367b2d286320bd03b8c2fbd3))

### Refactor

* refactor: typing basic containers, project name dash ([`7257bbf`](https://github.com/Rizhiy/replete/commit/7257bbf343b2123498d92ac6af0c80997430d55a))

### Test

* test: strict mypy typing ([`0bc0f8b`](https://github.com/Rizhiy/replete/commit/0bc0f8baf4c1a530e261c2194677bd2447097f2e))

* test: `types-xxhash`, updated pins ([`d73ddf9`](https://github.com/Rizhiy/replete/commit/d73ddf97cb99ce24ef6441e63218f66e16dd25aa))

### Unknown

* 0.12.2

Fix
* **consistent_hash:** Support classes in `consistent_hash` (ignore non-bound `_consistent_hash` methods) (6817fb0)

Documentation
* **README.md:** Fix badges (05664b2) ([`03be29a`](https://github.com/Rizhiy/replete/commit/03be29aee9e044992a0656be99e6ff2db74215fe))

* Merge branch &#39;fix_chash_typeobj&#39; into &#39;master&#39;

fix(consistent_hash): support classes in `consistent_hash` (ignore non-bound `_consistent_hash` methods)

See merge request utilities/nt-utils!27 ([`58a297b`](https://github.com/Rizhiy/replete/commit/58a297bb13d63715895f49132a1f966184c28f7c))

* Merge branch &#39;chore_refactor1_part3&#39; into &#39;master&#39;

chore: `doctest-modules` through pytest config

See merge request utilities/nt-utils!26 ([`2f067ea`](https://github.com/Rizhiy/replete/commit/2f067ea36f8b3e424e01f144bff4c5bb10308228))

* Merge branch &#39;chore_refactor1_part2&#39; into &#39;master&#39;

chore: yamlfix, typing containers fix

See merge request utilities/nt-utils!25 ([`c04af66`](https://github.com/Rizhiy/replete/commit/c04af66af233758ba93536d6b2b882053ee89b7d))

* Merge branch &#39;test_mypy_strict&#39; into &#39;master&#39;

test: strict mypy typing

See merge request utilities/nt-utils!24 ([`6b62bb5`](https://github.com/Rizhiy/replete/commit/6b62bb51046d25fe8b9a7afb60ec90e62cdf9859))

* Merge branch &#39;test_typeshed&#39; into &#39;master&#39;

test: `types-xxhash`, updated pins

See merge request utilities/nt-utils!23 ([`7fc1f88`](https://github.com/Rizhiy/replete/commit/7fc1f880dddb4612e5fa6aa6f85b7c6f2e46e5f8))

* Merge branch &#39;chore_refactor1&#39; into &#39;master&#39;

refactor: typing basic containers, project name dash

See merge request utilities/nt-utils!22 ([`02587a0`](https://github.com/Rizhiy/replete/commit/02587a025aca60bc6d1e4edf4663f3465e3f7a61))


## v0.12.1 (2022-02-17)

### Unknown

* 0.12.1

Fix
* **funcutils:** Fix `joinn_ffill` for the &#34;multiple right-side per one left-side&#34; case (49ab8b4) ([`89bb9d0`](https://github.com/Rizhiy/replete/commit/89bb9d07653f176f900a621d84260555b50d15bb))

* Merge branch &#39;fix_join_ffill&#39; into &#39;master&#39;

fix(funcutils): fix `join_ffill` for the &#34;multiple right-side per one left-side&#34; case

See merge request utilities/nt-utils!21 ([`6df397d`](https://github.com/Rizhiy/replete/commit/6df397d26d6b1b1f5502b4f312ffdc9c5127641d))


## v0.12.0 (2022-02-16)

### Feature

* feat(utils): `datetime_range` ([`340e0e2`](https://github.com/Rizhiy/replete/commit/340e0e2588794fd8b74968c9f25ddb6d7645a469))

### Fix

* fix(funcutils): fix `joinn_ffill` for the &#34;multiple right-side per one left-side&#34; case ([`49ab8b4`](https://github.com/Rizhiy/replete/commit/49ab8b4838a3f8e761a1168aca3100e71e2c8eee))

### Unknown

* 0.12.0

Feature
* **utils:** `datetime_range` (340e0e2) ([`c4af148`](https://github.com/Rizhiy/replete/commit/c4af14809057e559660500e45973faf5c4b7dda9))

* Merge branch &#39;feat_datetime_range&#39; into &#39;master&#39;

feat(utils): `datetime_range`

See merge request utilities/nt-utils!20 ([`3e043b2`](https://github.com/Rizhiy/replete/commit/3e043b20734592a075ae5c2321aa7160baec97a1))


## v0.11.0 (2022-02-11)

### Feature

* feat: `bisect_left`, `bisect_right` (`bisect` with `key=...` support) ([`c5f6dbd`](https://github.com/Rizhiy/replete/commit/c5f6dbdf88e17eee424c31a3dfe498f49c06d064))

### Test

* test: transpose the testing runs to avoid temporary effects ([`493cac5`](https://github.com/Rizhiy/replete/commit/493cac5897235154909ea2b3ead2c44dd9d3616a))

* test: reduce performance timing stochasticity by using the process time instead of wall time ([`2687cc1`](https://github.com/Rizhiy/replete/commit/2687cc12b2971cf8430c515fea83668aaa31f2a3))

### Unknown

* 0.11.0

Feature
* `bisect_left`, `bisect_right` (`bisect` with `key=...` support) (c5f6dbd) ([`d30aa24`](https://github.com/Rizhiy/replete/commit/d30aa242ff223ed8f4804d0adcd5d44bc7b47fa9))

* Merge branch &#39;test_process_time&#39; into &#39;master&#39;

test: reduce performance timing stochasticity by using the process time instead of wall time

See merge request utilities/nt-utils!19 ([`3c8e392`](https://github.com/Rizhiy/replete/commit/3c8e3928faf62c76e244192854dcab0d1f422a72))

* Merge branch &#39;feat_bisect&#39; into &#39;master&#39;

feat: `bisect_left`, `bisect_right` (`bisect` with `key=...` support)

See merge request utilities/nt-utils!16 ([`a529989`](https://github.com/Rizhiy/replete/commit/a529989c8a9ea9bd08049879274294ca51fb6b47))


## v0.10.0 (2022-02-11)

### Feature

* feat: py.typed marker ([`b1e6471`](https://github.com/Rizhiy/replete/commit/b1e6471ae5ed93cf9fca246c2fca616e6ae3fbc7))

### Refactor

* refactor: use basic containers for typing ([`7c6b9a3`](https://github.com/Rizhiy/replete/commit/7c6b9a3e96b029a0d059e83decaa2e6a0099800d))

### Test

* test: lenient mypy ([`57efa8a`](https://github.com/Rizhiy/replete/commit/57efa8afff10e501c927becd74c86ec083cf263a))

### Unknown

* 0.10.0

Feature
* Py.typed marker (b1e6471) ([`77dd4f2`](https://github.com/Rizhiy/replete/commit/77dd4f2f0b4b758752946e40234ee595d64eb429))

* Merge branch &#39;typing_basic_containers&#39; into &#39;master&#39;

refactor: use basic containers for typing

See merge request utilities/nt-utils!18 ([`2f00f4b`](https://github.com/Rizhiy/replete/commit/2f00f4bda247d893c0a7cd8e503feff56d214bef))

* Merge branch &#39;feat_py_typed&#39; into &#39;master&#39;

feat: py.typed marker

See merge request utilities/nt-utils!17 ([`7a0a88c`](https://github.com/Rizhiy/replete/commit/7a0a88cfec8770cf7e425a8f85a36b2744caaa62))

* Merge branch &#39;hhell/stuff1d&#39; into &#39;master&#39;

test: lenient mypy

See merge request utilities/nt-utils!15 ([`ac8b385`](https://github.com/Rizhiy/replete/commit/ac8b3852dee67e29e57466fd1ad0b84909ba4c7d))


## v0.9.1 (2022-02-01)

### Unknown

* 0.9.1

Feature
* **autocli:** Do not wrap into an additional function (4a28c73) ([`a502f4c`](https://github.com/Rizhiy/replete/commit/a502f4c6f5a43b7594c523b6cb2d11a10e159446))

* Merge branch &#39;hhell/stuff1a&#39; into &#39;master&#39;

imp(autocli): do not wrap into an additional function

See merge request utilities/nt-utils!14 ([`ef57fed`](https://github.com/Rizhiy/replete/commit/ef57feda0bfe0dd0a5ea0b4028e811382de22755))

* imp(autocli): do not wrap into an additional function ([`4a28c73`](https://github.com/Rizhiy/replete/commit/4a28c73ad1db6f1c36e6ab7ef9d84f55ca96c41c))


## v0.9.0 (2022-01-30)

### Chore

* chore: minor packaging fix ([`cc45a08`](https://github.com/Rizhiy/replete/commit/cc45a08fa71db47ed0e7ca3734d7c3481f998500))

### Feature

* feat(utils): `deep_update` (from `nt-dev`) ([`ccf455e`](https://github.com/Rizhiy/replete/commit/ccf455ecbbdbc6e1201effd7498627bdfbd3f152))

### Unknown

* 0.9.0

Feature
* **utils:** `deep_update` (from `nt-dev`) (ccf455e) ([`746b502`](https://github.com/Rizhiy/replete/commit/746b5023fae5e6f0fe623ad1f2301a0b5a22aded))

* Merge branch &#39;hhell/stuff1c&#39; into &#39;master&#39;

chore: minor packaging fix

See merge request utilities/nt-utils!12 ([`b93a314`](https://github.com/Rizhiy/replete/commit/b93a31449ef76e69f36f1f61b560c628c88c3422))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

feat(utils): `deep_update` (from `nt-dev`)

See merge request utilities/nt-utils!13 ([`70317ac`](https://github.com/Rizhiy/replete/commit/70317ac576407959089011bcd0c72cbb6486071a))


## v0.8.0 (2022-01-27)

### Style

* style: Format ([`0eaef60`](https://github.com/Rizhiy/replete/commit/0eaef60a76e9c1e8aac759d46327ce0ee4dbb406))

### Unknown

* 0.8.0

Feature
* **funcutils:** `merge_ffill`, `merge_backfill` (ddfdd10) ([`bf01923`](https://github.com/Rizhiy/replete/commit/bf019239f6214e41addd71365081a3ceff1b066d))

* Merge branch &#39;hhell/stuff1c&#39; into &#39;master&#39;

feat(funcutils): `merge_ffill`, `merge_backfill`

See merge request utilities/nt-utils!10 ([`9552187`](https://github.com/Rizhiy/replete/commit/955218700801d592f07a3145665540cfba26d374))


## v0.7.0 (2022-01-27)

### Style

* style(.isort.cfg): Add known_first_party ([`ae75941`](https://github.com/Rizhiy/replete/commit/ae75941749b92cbdf154cf92e8907089e6bcc74d))

### Unknown

* 0.7.0

Feature
* **cli:** `autocli` moved from `ntf` (03b90e7) ([`c70c3c8`](https://github.com/Rizhiy/replete/commit/c70c3c87a36d1f576293d7165aee4f89ed7fa5bf))

* Merge branch &#39;hhell/stuff1d&#39; into &#39;master&#39;

feat(cli): `autocli` moved from `ntf`

See merge request utilities/nt-utils!11 ([`49b2cd3`](https://github.com/Rizhiy/replete/commit/49b2cd3bdbce6d4406cb4aa87157c82a73080a98))


## v0.6.0 (2022-01-27)

### Feature

* feat(funcutils): `merge_ffill`, `merge_backfill` ([`ddfdd10`](https://github.com/Rizhiy/replete/commit/ddfdd10ba0b8aef04582b9102dc73f21c51097c5))

* feat(cli): `autocli` moved from `ntf` ([`03b90e7`](https://github.com/Rizhiy/replete/commit/03b90e7bbc164d28984b37bef7060e27a0f0b643))

* feat(utils): `ensure_unique_keys` ([`fbc6d06`](https://github.com/Rizhiy/replete/commit/fbc6d0603c422bb878ca4a761ab27394fa1bedc8))

### Style

* style: Format ([`6324e66`](https://github.com/Rizhiy/replete/commit/6324e66a8c47085354e2dafa9000a0012dca02ac))

### Unknown

* 0.6.0

Feature
* **utils:** `ensure_unique_keys` (fbc6d06) ([`c373fd9`](https://github.com/Rizhiy/replete/commit/c373fd90aa6baf011a3a790bbbcf26a87d204cd1))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

feat(utils): `ensure_unique_keys`

See merge request utilities/nt-utils!8 ([`1139bce`](https://github.com/Rizhiy/replete/commit/1139bcedda85869bc52352dde0e9ed9e056d97be))


## v0.5.0 (2022-01-25)

### Feature

* feat(aio): `alist`, `achunked` ([`e6abc30`](https://github.com/Rizhiy/replete/commit/e6abc306d62e4111c5f7fb9985261b690ee750e1))

### Unknown

* 0.5.0

Feature
* **aio:** `alist`, `achunked` (e6abc30) ([`e875fb4`](https://github.com/Rizhiy/replete/commit/e875fb48dd87d8ecc555b0cf62776caf4c7953f6))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

feat(aio): `alist`, `achunked`

See merge request utilities/nt-utils!6 ([`500a30c`](https://github.com/Rizhiy/replete/commit/500a30c308bb8b7dac388807c651aacd86c8a90f))


## v0.4.1 (2022-01-25)

### Fix

* fix: fixed tests, updated pins ([`ef00a12`](https://github.com/Rizhiy/replete/commit/ef00a125996b698d65d992c90f79a54ec2a03c22))

### Unknown

* 0.4.1

Fix
* Fixed tests, updated pins (ef00a12) ([`8bc1f9e`](https://github.com/Rizhiy/replete/commit/8bc1f9e3cc9da4ff64ef4c2f67c159f756690023))

* Merge branch &#39;hhell/stuff1b&#39; into &#39;master&#39;

fix: fixed tests, updated pins

See merge request utilities/nt-utils!7 ([`ce66c49`](https://github.com/Rizhiy/replete/commit/ce66c4965028bea4886090a05a12ba7fdae774f6))


## v0.4.0 (2022-01-14)

### Feature

* feat: `nt_utils.aio.LazyWrapAsync` ([`25dc290`](https://github.com/Rizhiy/replete/commit/25dc290e60a72c5ff5cecc80d6c9f25727e2ec58))

### Unknown

* 0.4.0

Feature
* `nt_utils.aio.LazyWrapAsync` (25dc290) ([`0610ccf`](https://github.com/Rizhiy/replete/commit/0610ccfe836817dcd4d76871f1e9d936fee354f5))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

feat: `nt_utils.aio.LazyWrapAsync`

See merge request utilities/nt-utils!5 ([`cd3a4b2`](https://github.com/Rizhiy/replete/commit/cd3a4b2508113c8909e1c89f52fb360f4e037df5))


## v0.3.0 (2022-01-12)

### Feature

* feat(utils): `chunks`, `date_range` ([`cc7d203`](https://github.com/Rizhiy/replete/commit/cc7d2036e84475e75d7f0b5042e94a291f7f156e))

### Unknown

* 0.3.0

Feature
* **utils:** `chunks`, `date_range` (cc7d203) ([`5dbe390`](https://github.com/Rizhiy/replete/commit/5dbe390dbd00c8ca51aef9fb547ccea294d85783))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

feat(utils): `chunks`, `date_range`

See merge request utilities/nt-utils!4 ([`9ab822d`](https://github.com/Rizhiy/replete/commit/9ab822df8f6bfcf0ddeecb8f4a1b6cd645afd780))


## v0.2.0 (2021-12-24)

### Feature

* feat: consistent_hash moved from `nt_cache` ([`746fb21`](https://github.com/Rizhiy/replete/commit/746fb212d7b5fdf8db2fd96608cb3a6ad523d804))

### Unknown

* 0.2.0

Feature
* Consistent_hash moved from `nt_cache` (746fb21) ([`f6c03d1`](https://github.com/Rizhiy/replete/commit/f6c03d12a082a5d21baab703d47021a59100e5c9))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

feat: consistent_hash moved from `nt_cache`

See merge request utilities/nt-utils!3 ([`70c06f4`](https://github.com/Rizhiy/replete/commit/70c06f403abf92ca817bff8714949f6d1eda1f82))


## v0.1.1 (2021-12-17)

### Chore

* chore: minor cleanup ([`37ea2df`](https://github.com/Rizhiy/replete/commit/37ea2dff4acbf9c517e8f08a4ac4cf74546c167a))

* chore: packaging by flit, from python-repo template ([`4a9e8ad`](https://github.com/Rizhiy/replete/commit/4a9e8ad6f4409a4afd86d79cfeb548a7b787c6c1))

### Unknown

* 0.1.1

Feature
* Requirements.txt (4fbc960) ([`0d05fa8`](https://github.com/Rizhiy/replete/commit/0d05fa89ec09ed058b0d670f3c74a13a3eb804b3))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

chore: packaging by flit, from python-repo template

See merge request utilities/nt-utils!2 ([`a440a65`](https://github.com/Rizhiy/replete/commit/a440a65f0ac6f1d2249dfb8641dfdfc4d2232c25))

* imp: requirements.txt ([`4fbc960`](https://github.com/Rizhiy/replete/commit/4fbc9606d3fe1a34653c4180eb267ebf761bb8c0))


## v0.1.0 (2021-12-13)

### Feature

* feat: `grouped()` ([`584e34e`](https://github.com/Rizhiy/replete/commit/584e34e0554e1884219444eeb1034bc855eaaf61))

### Fix

* fix(setup.cfg): Add version_variable ([`0e83dd2`](https://github.com/Rizhiy/replete/commit/0e83dd29e0b81d32eb6b7bd4333a8fe9bbc7d90a))

* fix: Fix cfg name ([`b469ca6`](https://github.com/Rizhiy/replete/commit/b469ca6f205364c288d93c5cdf3c2bccd2bb5ee4))

### Unknown

* 0.1.0

Feature
* `grouped()` (584e34e)

Fix
* **setup.cfg:** Add version_variable (0e83dd2)
* Fix cfg name (b469ca6) ([`8ff3a8b`](https://github.com/Rizhiy/replete/commit/8ff3a8b1a66026613dc48f9671056c8d5f856758))

* Merge branch &#39;hhell/stuff&#39; into &#39;master&#39;

feat: `grouped()`

See merge request utilities/nt-utils!1 ([`ef1538d`](https://github.com/Rizhiy/replete/commit/ef1538d3a933314f655294495f078e64bc266580))

* 0.0.0 ([`2a248b3`](https://github.com/Rizhiy/replete/commit/2a248b3ba0cbe8f1b0fed375c92b8a04cb97472e))

* Initial commit ([`6d22445`](https://github.com/Rizhiy/replete/commit/6d22445f6588ed8c6707bb3d28d7efd7a45a8074))
