1
00:00:00,360 --> 00:00:02,29
So far we've seen how you can

2
00:00:02,29 --> 00:00:03,588
use CSS to style your text,

3
00:00:04,88 --> 00:00:05,904
but we can also use CSS to completely

4
00:00:05,904 --> 00:00:07,500
change the layout of our page.

5
00:00:07,620 --> 00:00:09,148
That means we can move things around,

6
00:00:09,157 --> 00:00:10,187
change the size,

7
00:00:10,187 --> 00:00:11,777
even put things on top of each other.

8
00:00:12,10 --> 00:00:13,551
But what are the things

9
00:00:13,551 --> 00:00:14,401
we want to move around?

10
00:00:14,498 --> 00:00:16,117
Sometimes they're elements

11
00:00:16,117 --> 00:00:17,339
that we've already made,

12
00:00:17,339 --> 00:00:18,811
like a certain paragraph,

13
00:00:18,812 --> 00:00:20,672
or a certain heading.

14
00:00:21,231 --> 00:00:22,365
But often times,

15
00:00:22,445 --> 00:00:24,679
they're a group of elements that we've made,

16
00:00:24,679 --> 00:00:26,889
like a selection of text,

17
00:00:27,55 --> 00:00:30,64
or a heading and a few paragraphs.

18
00:00:31,693 --> 00:00:32,946
In order to move them

19
00:00:32,946 --> 00:00:34,364
around together as a unit,

20
00:00:34,365 --> 00:00:36,785
we need to introduce two new HTML tags.

21
00:00:36,805 --> 00:00:39,225
Which we call the grouping elements.

22
00:00:39,246 --> 00:00:41,460
We didn't talk about them before CSS,

23
00:00:41,460 --> 00:00:42,662
because they're only useful

24
00:00:42,662 --> 00:00:44,210
when combined with CSS.

25
00:00:44,210 --> 00:00:46,555
They have no semantic meaning to the browser.

26
00:00:47,275 --> 00:00:49,176
The first tag, is the <span> tag,

27
00:00:49,596 --> 00:00:51,516
and it's what we use for grouping

28
00:00:51,516 --> 00:00:52,756
a selection of text.

29
00:00:53,244 --> 00:00:54,193
Let's say we want a colour,

30
00:00:54,193 --> 00:00:56,503
that's word "Love Red".

31
00:00:57,55 --> 00:00:58,692
And we just want to colour the word,

32
00:00:58,692 --> 00:00:59,952
not the rest of the heading.

33
00:01:00,327 --> 00:01:02,458
We'll put our cursor before "Love",

34
00:01:02,458 --> 00:01:06,138
type the start tag for <span>.

35
00:01:06,499 --> 00:01:10,518
Put it after, type the end tag, okay.

36
00:01:10,678 --> 00:01:11,643
Now we want to style this

37
00:01:11,644 --> 00:01:12,809
<span> of characters.

38
00:01:13,8 --> 00:01:14,643
We could make a rule to colour all <span>s

39
00:01:14,723 --> 00:01:15,679
on the page,

40
00:01:15,780 --> 00:01:18,558
but we may not want them all to be red.

41
00:01:18,558 --> 00:01:19,980
Let's give the <span> a

42
00:01:20,107 --> 00:01:21,980
class of "lovey-dovey",

43
00:01:25,86 --> 00:01:29,53
and add a rule just for elements that

44
00:01:29,53 --> 00:01:30,369
have the class "lovey-dovey".

45
00:01:30,388 --> 00:01:33,755
So, .lovey-dovey, color: red.

46
00:01:34,613 --> 00:01:36,703
Look at how lovey dovey that text is now!

47
00:01:38,93 --> 00:01:39,667
So <span>s are good for grouping

48
00:01:39,667 --> 00:01:41,717
selections of text, how do we group a

49
00:01:41,727 --> 00:01:43,187
bunch of elements together?

50
00:01:43,507 --> 00:01:45,247
That's where the <div> tag comes in.

51
00:01:45,680 --> 00:01:46,747
Let's say we want to group

52
00:01:46,747 --> 00:01:47,717
this bottom section.

53
00:01:48,195 --> 00:01:49,464
The official info header, and

54
00:01:49,464 --> 00:01:51,173
the paragraphs and picture below it.

55
00:01:51,743 --> 00:01:52,714
To do that,

56
00:01:52,714 --> 00:01:58,129
I'll put my cursor before the h3 and do

57
00:01:58,129 --> 00:01:59,389
the start tag for <div>.

58
00:01:59,859 --> 00:02:02,259
And then go down to the final paragraph,

59
00:02:02,690 --> 00:02:04,620
and right the end tag for <div>.

60
00:02:05,467 --> 00:02:07,847
We have a <div>, now we need to style it.

61
00:02:08,509 --> 00:02:09,567
To style the <div>,

62
00:02:09,568 --> 00:02:11,426
I'm going to give it an ID.

63
00:02:11,426 --> 00:02:13,516
"official-info".

64
00:02:15,117 --> 00:02:16,417
Then add a rule for it up here.

65
00:02:16,422 --> 00:02:21,102
So #official-info, and background.

66
00:02:22,275 --> 00:02:23,715
Let's make it a nice grey.

67
00:02:23,884 --> 00:02:26,934
Let's pick out... this... That's good.

68
00:02:27,133 --> 00:02:28,646
So now you can see the <div> has become

69
00:02:28,646 --> 00:02:30,840
a grey box containing all of the elements

70
00:02:30,841 --> 00:02:31,681
inside of it.

71
00:02:31,772 --> 00:02:34,267
And it's different from if we give each of

72
00:02:34,267 --> 00:02:35,947
them a grey background separately.

73
00:02:35,998 --> 00:02:38,227
If we did that, there would be a space in

74
00:02:38,228 --> 00:02:39,308
between them that wouldn't go gray.

75
00:02:39,520 --> 00:02:41,120
We have to make a <div>,

76
00:02:41,129 --> 00:02:42,909
if we want a box around everything.

77
00:02:44,708 --> 00:02:46,185
You can think of <span>,

78
00:02:46,185 --> 00:02:47,735
as being for grouping text.

79
00:02:48,303 --> 00:02:50,759
And you can think of <div>,

80
00:02:50,759 --> 00:02:52,268
for grouping elements.

81
00:02:52,478 --> 00:02:54,718
But there's another way to distinguish them as well.

82
00:02:55,451 --> 00:02:56,853
You see there are two types

83
00:02:56,854 --> 00:02:58,104
of elements in the CSS world.

84
00:02:58,412 --> 00:03:00,232
Inline and block.

85
00:03:00,499 --> 00:03:03,409
An inline element does not have a new line after it.

86
00:03:03,570 --> 00:03:06,726
Like if you make a multiple of them they will all be on the same line.

87
00:03:06,726 --> 00:03:08,751
A few examples we have talked about are

88
00:03:08,751 --> 00:03:11,651
a and image.

89
00:03:11,832 --> 00:03:13,432
And you can see with this image,

90
00:03:13,451 --> 00:03:16,430
how it just runs into the text next to it.

91
00:03:16,616 --> 00:03:18,326
There's no new line after it.

92
00:03:18,657 --> 00:03:21,887
A block element does have a line after it,

93
00:03:21,912 --> 00:03:24,602
and that is what most HTML tags create.

94
00:03:24,818 --> 00:03:26,978
Look at all the examples on this page.

95
00:03:27,41 --> 00:03:30,281
The headings, the paragraphs, the list.

96
00:03:30,799 --> 00:03:33,699
The browser put new lines after all of them,

97
00:03:33,732 --> 00:03:36,152
without you needing to write a <br> tag.

98
00:03:37,27 --> 00:03:39,39
What does that have to do with <span>,

99
00:03:39,39 --> 00:03:39,726
and <div>?

100
00:03:39,835 --> 00:03:43,203
Well a <span> creates an inline element,

101
00:03:43,203 --> 00:03:47,123
and a <div> creates a block element.

102
00:03:47,252 --> 00:03:49,492
That means, that if you add a <div>,

103
00:03:49,492 --> 00:03:53,432
and don't add any other style,

104
00:03:53,940 --> 00:03:56,270
the browser will blockify

105
00:03:56,270 --> 00:03:58,145
that part of the page.

106
00:03:58,145 --> 00:04:00,534
Like that bit of text just wrapped in a <div>,

107
00:04:00,534 --> 00:04:02,983
now has new lines before and after.

108
00:04:02,998 --> 00:04:05,495
And maybe that's what you want,

109
00:04:05,495 --> 00:04:07,525
just keep this difference in mind.

110
00:04:07,553 --> 00:04:09,383
And keep going, because there's a lot more

111
00:04:09,395 --> 00:04:10,885
we can do with these tags.

112
00:04:10,885 --> 00:04:12,631
Especially the might <div>.

113
00:04:12,631 --> 00:04:14,000
Captioned by: 5A Jasmine :) aka JP 4B :)

