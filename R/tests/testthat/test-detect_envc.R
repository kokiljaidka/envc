test_that("stage directions detected", {
  r <- detect_envc("*hugs* you're the best")
  expect_true(r$stage_direction)
  expect_true(r$kinesics)
})

test_that("plain text returns all FALSE", {
  r <- detect_envc("The meeting is at 3pm.")
  expect_false(r$any_envc)
})

test_that("emoji faces detected", {
  r <- detect_envc("love this \U0001F60A")
  expect_true(r$emoji_faces)
})

test_that("vocalics detected", {
  expect_true(detect_envc("lol that's funny")$vocalics)
  expect_true(detect_envc("ugh not again")$vocalics)
  expect_true(detect_envc("omg really")$vocalics)
})

test_that("intensity caps excludes acronyms", {
  expect_true(detect_envc("THIS IS AMAZING")$intensity_caps)
  expect_false(detect_envc("I work in IT at NASA")$intensity_caps)
})

test_that("intensity punctuation detected", {
  expect_true(detect_envc("what!! no way!!")$intensity_punctuation)
  expect_true(detect_envc("oh???")$intensity_punctuation)
  expect_false(detect_envc("hello.")$intensity_punctuation)
})

test_that("elongation detected", {
  expect_true(detect_envc("I loooove this")$elongation)
  expect_false(detect_envc("I love this")$elongation)
})

test_that("ellipsis detected", {
  expect_true(detect_envc("well... okay")$ellipsis)
  expect_false(detect_envc("well okay")$ellipsis)
})

test_that("paper example: Friday post", {
  r <- detect_envc("Today is Friday!!!!!!! thannkkkk gooood")
  expect_true(r$intensity_punctuation)
  expect_true(r$elongation)
})

test_that("paper example: EXAMS post", {
  r <- detect_envc("EXAAAAAAAAAMS \U0001F622")
  expect_true(r$intensity_caps)
  expect_true(r$elongation)
  expect_true(r$emoji_faces)
})

test_that("paper example: tired post", {
  r <- detect_envc("Oh I am soo tiiiired ughh wow...")
  expect_true(r$elongation)
  expect_true(r$vocalics)
  expect_true(r$ellipsis)
})

test_that("counts work", {
  r <- detect_envc_counts("love \U0001F60D\U0001F60D\U0001F60D")
  expect_equal(r$emoji_faces, 3L)
})

test_that("annotate_envc works on data frame", {
  df <- data.frame(text = c("hello!!", "OMG \U0001F60D", "plain"), stringsAsFactors = FALSE)
  result <- annotate_envc(df)
  expect_true("any_envc" %in% names(result))
  expect_true(result$intensity_punctuation[1])
  expect_false(result$any_envc[3])
})
